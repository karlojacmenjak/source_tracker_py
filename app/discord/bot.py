import os
from typing import Dict

from discord import Bot

from core.constant import EnviormentVariables


class SourceTrackerBot(Bot):
    def __init__(self, description=None, *args, **options) -> None:
        super().__init__(description, *args, **options)

    async def on_ready(self) -> None:
        print(
            "\nDiscord bot logged in as:",
            f"{self.user.name} with user id {self.user.id}",
            sep="\n",
        )

    async def guild_count(self) -> int:
        return len(self.guilds)


def create_bot() -> SourceTrackerBot:
    _bot = SourceTrackerBot()
    return _bot


async def run_bot() -> None:
    token_env = EnviormentVariables.bot_token

    if os.environ[token_env] is None:
        raise RuntimeError(f"Enviornment variable `{token_env}` is set to None")

    await bot.start(os.environ[token_env])


bot = create_bot()
