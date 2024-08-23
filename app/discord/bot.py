import os
from pathlib import Path

import discord
from discord.ext import commands

from core.constant import AppConstants, DiscordAPI


class SourceTrackerBot(commands.Bot):
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
        is_in_guild = guild_id in self.get_guild_ids()
        return is_in_guild

    def check_perms(self, guild_id: int, user_id: int) -> bool:
        guild = self.get_guild(guild_id)
        if not guild:
            return False

        member = guild.get_member(user_id)
        if not member or not member.guild_permissions.administrator:
            return False
        return True


def create_bot() -> SourceTrackerBot:
    rel_path = ["app", "discord", "cogs"]
    path = os.path.join(os.getcwd(), *rel_path)
    cogs_list = [
        Path(filename).stem
        for filename in os.listdir(path)
        if filename.startswith("cog_")
    ]

    _bot = SourceTrackerBot()
    _bot.help_command = None

    for cog in cogs_list:
        cog_path = f"{'.'.join(rel_path)}.{cog}"
        print("Adding cog:", cog_path)
        _bot.load_extension(cog_path)

    print("Cogs added to bot", "Bot created sucessfully", sep="\n")
    return _bot


async def run_bot() -> None:
    token_env = DiscordAPI.bot_token

    if os.environ[token_env] is None:
        raise RuntimeError(f"Enviornment variable `{token_env}` is set to None")

    print("Starting bot")
    try:
        await bot.start(os.environ[token_env])
    except KeyboardInterrupt:
        await bot.close()
    print("Bot started!")


bot = create_bot()
