import json
from datetime import datetime, timedelta
from random import randint

import discord
import humanize
from discord.ext import commands, tasks
from tablib import Dataset

from app.discord.cogs.embeds.embeds import ServerInfoEmbed
from app.models.database import ValidGameServer
from app.models.form import GameServer
from core.constant import DashboardConstants
from core.database.local_database import local_db
from core.factory.controller_factory import ControllerFactory


async def autocomplete_server(ctx: discord.AutocompleteContext) -> list[str]:
    choices: list[discord.OptionChoice] = []
    response = await local_db.get_game_servers(ctx.interaction.guild_id)

    for server in response:
        s = {"address": server.address, "port": server.port}
        choices.append(
            discord.OptionChoice(name=server.server_name, value=json.dumps(s))
        )

    return choices


class CogGameServer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.fetch_server_info.start()
        self.controller = ControllerFactory.get_gameserver_controller()

    def cog_unload(self) -> None:
        self.fetch_server_info.cancel()
        return super().cog_unload()

    @tasks.loop(minutes=DashboardConstants.check_period_min)
    async def fetch_server_info(self) -> None:
        for guild in self.bot.guilds:
            stats_channel = (
                guild.system_channel if guild.system_channel else guild.channels[0]
            )
            game_servers_info: list[ValidGameServer] = []

            bot_settings = await local_db.get_bot_settings(guild_id=guild.id)
            if not bot_settings:
                continue

            _, enable_features, check_period = bot_settings

            if not enable_features:
                continue

            game_servers = await local_db.get_game_servers(guild_id=guild.id)
            for server in game_servers:

                if self.info_check_required(check_period, server.last_data_fetch):
                    try:
                        valid_server = await self.refresh_info(server)
                        game_servers_info.append(valid_server)

                        await local_db.update_game_server_last_fetch(
                            server, valid_server
                        )
                    except Exception as e:
                        print(e)
                else:
                    game_servers_info.append(
                        ValidGameServer.model_validate_json(
                            server.last_response, strict=False
                        )
                    )

            if len(game_servers_info) > 0:
                await stats_channel.send(
                    embed=(ServerInfoEmbed(self.bot, guild, game_servers_info))
                )

    @fetch_server_info.before_loop
    async def before_fetch_server_info(self) -> None:
        await self.bot.wait_until_ready()

    @commands.guild_only()
    @commands.slash_command(
        usage="/peek <servername>",
        description="Peeks into server, showing players in it\n`/peek <servername>`",
    )
    @discord.option(
        name="server",
        description="Pick a server",
        autocomplete=autocomplete_server,
    )
    async def peek(self, ctx: discord.ApplicationContext, server: str) -> None:
        server: GameServer = GameServer.model_validate_json(server)
        game_servers = await local_db.get_game_servers(
            guild_id=ctx.interaction.guild_id
        )

        server = next(
            filter(
                lambda g: g.address == server.address and g.port == server.port,
                game_servers,
            )
        )

        players = await self.controller.get_server_players(server)
        players = sorted(players, key=lambda p: p.score, reverse=True)

        data = Dataset(headers=["Username", "Score", "Time playing"])

        for p in players:
            data.append([p.name, p.score, humanize.naturaldelta(p.duration)])
        message = f"```Current players in {server.server_name}```"
        message += "```" + data.export("cli", tablefmt="github") + "```"

        await ctx.respond(message)

    async def refresh_info(self, server: GameServer) -> ValidGameServer:
        return await self.controller.get_server_info(server)

    def info_check_required(
        self, check_period, last_data_fetch: datetime | None
    ) -> bool:
        if not last_data_fetch:
            return True
        expected_datetime = last_data_fetch + timedelta(minutes=check_period)
        check_period_passed = expected_datetime < datetime.now()
        return check_period_passed


def setup(bot: commands.Bot) -> None:
    bot.add_cog(CogGameServer(bot))
