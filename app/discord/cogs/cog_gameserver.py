from datetime import datetime, timedelta

from discord import Bot, Embed, EmbedField, Guild
from discord.ext import commands, tasks

from app.models.database import ValidGameServer
from app.models.form import GameServer
from core.constant import BotConstants, DashboardConstants
from core.database.local_database import local_db
from core.factory.controller_factory import ControllerFactory


class ServerInfoEmbed(Embed):
    def __init__(
        self, bot: Bot, guild: Guild, game_servers: list[ValidGameServer]
    ) -> None:
        title = f"{guild.name}'s list of Source Engine Game Info's"

        game_servers = sorted(game_servers, key=lambda g: g.player_count, reverse=True)

        fields: list[EmbedField] = []
        for s in game_servers:
            fields.append(
                EmbedField(
                    name=s.server_name,
                    value=f"""***Game***: {s.game}\n
                        ***Player count***: {s.player_count}/{s.max_players}\n
                        Join server using the following command:\n```connect {s.address}:{s.port}```\n\n
                        \u200b""",
                    inline=False,
                )
            )

        super().__init__(
            title=title,
            color=BotConstants.color,
            timestamp=datetime.now(),
            thumbnail=bot.user.avatar.url,
            fields=fields,
        )


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
                        valid_server = await self.refresh_info(
                            game_servers_info, server
                        )
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

    async def refresh_info(
        self, game_servers_info: list[ValidGameServer], server: GameServer
    ) -> ValidGameServer:
        info = await self.controller.get_server_info(server)
        game_servers_info.append(info)
        return info

    def info_check_required(self, check_period, last_data_fetch: datetime) -> bool:
        if not last_data_fetch:
            return True
        expected_datetime = last_data_fetch + timedelta(minutes=check_period)
        check_period_passed = expected_datetime < datetime.now()
        return check_period_passed

    @fetch_server_info.before_loop
    async def before_fetch_server_info(self) -> None:
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(CogGameServer(bot))
