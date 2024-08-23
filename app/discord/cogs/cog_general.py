from datetime import datetime

import discord
from discord.ext import commands

from core.constant import AppConstants, BotConstants


class OnJoinEmbed(discord.Embed):
    def __init__(self, bot: commands.Bot) -> None:

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
    def __init__(self, bot: commands.Bot) -> None:
        title = f"{BotConstants.name} Help"
        description = "Here's the list of all available slash commands:"

        for c in bot.walk_application_commands():
            print(c.name, c)

        super().__init__(
            title=title,
            description=description,
            color=BotConstants.color,
            timestamp=datetime.now(),
            image=bot.user.avatar.url,
        )


class CogGeneral(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        if guild.system_channel:
            await guild.system_channel.send("", embed=OnJoinEmbed(self.bot))

    @commands.command(usage="/help", description="My description to display")
    async def help(self, ctx: discord.ApplicationContext) -> None:
        await ctx.send("A")
        # await ctx.respond("", embed=HelpEmbed(self.bot))

    @commands.command()
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.send("`Test completed succesfully`")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(CogGeneral(bot))
