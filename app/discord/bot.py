import os

from discord import Bot

from core.constant import EnviormentVariables


class SourceTrackerBot(Bot):
    def __init__(self, description=None, *args, **options) -> None:
        super().__init__(description, *args, **options)

    async def on_ready(self) -> None:
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")


def create_bot() -> SourceTrackerBot:
    _bot = SourceTrackerBot()
    return _bot


def run_bot() -> None:
    token_env = EnviormentVariables.bot_token

    if os.environ[token_env] is None:
        raise RuntimeError(f"Enviornment variable `{token_env}` is set to None")

    bot.run(os.environ[token_env])


bot = create_bot()
