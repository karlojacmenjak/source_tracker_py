from datetime import datetime

import discord
from discord import Embed, EmbedField, Guild
from discord.ext.commands import Bot

from app.models.database import ValidGameServer
from core.constant import AppConstants, BotConstants


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


class OnJoinEmbed(discord.Embed):
    def __init__(self, bot: Bot) -> None:

        description = f"""Thank you for adding Source Tracker to your guild! \n\n
        To start using this bot, use `/help` to display available Source Trackers Slash Commands!\n\n
        Please go to <http:/{AppConstants.host}:{AppConstants.port}/> to customize Source Tracker's features."""

        super().__init__(
            title=BotConstants.name,
            description=description,
            color=BotConstants.color,
            timestamp=datetime.now(),
            author=discord.EmbedAuthor(
                name="Source Tracker", icon_url=bot.user.avatar.url
            ),
        )


class HelpEmbed(discord.Embed):
    def __init__(self, bot: Bot) -> None:
        title = f"{BotConstants.name} Help"
        description = "Here's the list of all available slash commands:"

        embed_fields: list[discord.EmbedField] = []

        for c in bot.walk_application_commands():
            embed_fields.append(discord.EmbedField(name=c.name, value=c.description))

        super().__init__(
            title=title,
            description=description,
            color=BotConstants.color,
            timestamp=datetime.now(),
            thumbnail=bot.user.avatar.url,
            fields=embed_fields,
        )
