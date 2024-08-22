import os

import discord
from discord import Bot

from core.constant import AppConstants, DiscordAPI


class SourceTrackerBot(Bot):
    def __init__(self, description=None, *args, **options) -> None:
        intents = discord.Intents.default()
        intents.members = AppConstants.production
        super().__init__(intents=intents, description=description, *args, **options)

    async def on_ready(self) -> None:
        print(
            "\nDiscord bot logged in as:",
            f"{self.user.name} with user id {self.user.id}",
            sep="\n",
        )

    def guild_count(self) -> int:
        return self.guilds.__len__()

    def get_guild_ids(self) -> list[int]:
        return [guild.id for guild in self.guilds]

    def is_in_guild(self, guild_id: int) -> bool:
        return guild_id in self.guilds

    async def check_perms(self, guild_id: int, user_id: int) -> bool:
        guild = self.get_guild(guild_id)
        if not guild:
            return False

        member = guild.get_member(user_id)
        if not member or not member.guild_permissions.administrator:
            return False
        return True


def create_bot() -> SourceTrackerBot:
    _bot = SourceTrackerBot()
    return _bot


async def run_bot() -> None:
    token_env = DiscordAPI.bot_token

    if os.environ[token_env] is None:
        raise RuntimeError(f"Enviornment variable `{token_env}` is set to None")

    await bot.start(os.environ[token_env])


bot = create_bot()
