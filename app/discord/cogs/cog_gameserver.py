from discord.ext import commands, tasks

from core.constant import DashboardConstants


class CogGameServer(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.fetch_server_info.start()

    def cog_unload(self) -> None:
        self.fetch_server_info.cancel()
        return super().cog_unload()

    @tasks.loop(seconds=DashboardConstants.check_period_min)
    async def fetch_server_info(self) -> None:
        print("Hello world")

    @fetch_server_info.before_loop
    async def before_printer(self) -> None:
        await self.bot.wait_until_ready()


def setup(bot: commands.Bot) -> None:
    bot.add_cog(CogGameServer(bot))
