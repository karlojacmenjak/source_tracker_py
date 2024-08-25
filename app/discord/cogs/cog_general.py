import discord
from discord.ext import commands

from app.discord.cogs.helpers.embeds import (
    HelpEmbed,
    OnJoinEmbed,
    RequestEmbed,
    WatchlistEmbed,
)
from app.discord.cogs.helpers.views import RequestView
from app.models.database import ValidGameServer
from app.models.form import GameServer
from core.database.local_database import local_db
from core.factory.controller_factory import ControllerFactory


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
        description="Tests if bot is alive or dead, like a that one guys cat!\nUsage: `/test`",
    )
    async def test(self, ctx: discord.ApplicationContext):
        await ctx.respond("`Test completed succesfully` ||Also I am not a cat||")

    @commands.slash_command(
        usage="/watchlist",
        description="Displays all Source Engine servers this guild is tracking\nUsage: `/watchlist`",
    )
    async def watchlist(self, ctx: discord.ApplicationContext):
        servers = await local_db.get_game_servers_by_guild(
            guild_id=ctx.interaction.guild_id
        )

        await ctx.respond(
            embed=WatchlistEmbed(self.bot, ctx.interaction.guild, servers)
        )

    @commands.slash_command(
        usage="/request",
        description="Request adding a Source Engine game server to watchlist\nUsage: `/request <address> <port>`",
    )
    @discord.option(
        name="address",
        input_type=str,
    )
    @discord.option(
        name="port",
        input_type=int,
    )
    async def request(
        self, ctx: discord.ApplicationContext, address: str, port: int
    ) -> None:
        await ctx.defer(ephemeral=False)
        controller = ControllerFactory.get_gameserver_controller()
        server = GameServer(address=address, port=port)

        db_server = await local_db.get_game_server(server)

        valid_server: ValidGameServer | None = None
        if db_server:
            valid_server = ValidGameServer(**db_server.model_dump())
        else:
            try:
                valid_server = await controller.get_server_info(server)
                await local_db.add_game_servers([valid_server])
            except Exception as e:
                pass

        view = RequestView(server=valid_server)

        if valid_server:
            await ctx.send_followup(
                view=view, embed=RequestEmbed(ctx, valid_server), ephemeral=False
            )
            return
        await ctx.send_followup(
            "Server is not valid, please enter a valid server address and port!",
            ephemeral=True,
        )


def setup(bot: commands.Bot) -> None:
    bot.add_cog(CogGeneral(bot))
