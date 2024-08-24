import discord

from app.discord.cogs.helpers.buttons import ActionButton


class RequestView(discord.ui.View):

    def __init__(self) -> None:
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

    def accept(self):
        self.clear_items()

    def deny(self):
        self.clear_items()
