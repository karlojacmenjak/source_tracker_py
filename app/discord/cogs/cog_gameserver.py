from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks

from app.discord.cogs.embeds.embeds import ServerInfoEmbed
from app.models.database import ValidGameServer
from app.models.form import GameServer
from core.constant import DashboardConstants
from core.database.local_database import local_db
from core.factory.controller_factory import ControllerFactory


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
                        game_servers.append(valid_server)

                        await local_db.update_game_server_last_fetch(
                            server, valid_server
                        )
                    except Exception as e:
                        print(e)
                else:
                    game_servers.append(
                        ValidGameServer.model_validate_json(server.last_response)
                    )

            if len(game_servers_info) > 0:
                await stats_channel.send(
                    embed=(ServerInfoEmbed(self.bot, guild, game_servers_info))
                )

    @fetch_server_info.before_loop
    async def before_fetch_server_info(self) -> None:
        await self.bot.wait_until_ready()

    @commands.slash_command(
        usage="/peek <servername>",
        description="Peeks into server, showing players in it\n`/peek <servername>`",
    )
    async def peek(self, ctx: discord.ApplicationContext):
        await ctx.respond()

    async def refresh_info(self, server: GameServer) -> ValidGameServer:
        return await self.controller.get_server_info(server)

    def info_check_required(self, check_period, last_data_fetch: datetime) -> bool:
        if not last_data_fetch:
            return True
        expected_datetime = last_data_fetch + timedelta(minutes=check_period)
        check_period_passed = expected_datetime < datetime.now()
        return check_period_passed


def setup(bot: commands.Bot) -> None:
    bot.add_cog(CogGameServer(bot))
