import discord
from discord.ext import commands

from app.discord.cogs.embeds.embeds import HelpEmbed, OnJoinEmbed


class CogGeneral(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        if guild.system_channel:
            await guild.system_channel.send("", embed=OnJoinEmbed(self.bot))

    @commands.slash_command(
        usage="/help", description="Displays all available commands\n Usage: `/help`"
    )
    async def help(self, ctx: discord.ApplicationContext) -> None:
        await ctx.respond(embed=HelpEmbed(self.bot))

    @commands.slash_command(
        usage="/test",
        description="Tests if bot is alive or dead, like a that one guys cat!\nUsage: /test",
    )
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("`Test completed succesfully` ||Also I am not a cat||")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(CogGeneral(bot))
