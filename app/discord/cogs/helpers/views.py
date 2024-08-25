import discord

from app.discord.cogs.helpers.buttons import ActionButton
from app.models.database import ValidGameServer
from core.database.local_database import local_db


class RequestView(discord.ui.View):

    def __init__(self, server: ValidGameServer) -> None:
        self.server = server
        super().__init__()
        self.add_item(
            ActionButton(
                label="Accept",
                style=discord.ButtonStyle.green,
                custom_callback=self.accept,
            )
        )
        self.add_item(
            ActionButton(
                label="Deny",
                style=discord.ButtonStyle.red,
                custom_callback=self.deny,
            )
        )

    async def accept(self) -> None:
        await self.save_to_database()
        await self.message.edit(
            f"{self.server.server_name} was successfully accepted",
            embed=None,
            view=None,
        )

    async def save_to_database(self):
        await local_db.add_settings_game_servers(self.message.guild.id, [self.server])

    async def deny(self):
        await self.message.delete()
