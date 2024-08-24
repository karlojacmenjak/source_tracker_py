import discord


class ActionButton(discord.ui.Button):
    def __init__(self, label: str, style: discord.ButtonStyle) -> None:
        super().__init__(
            label=label,
            style=style,
        )

    async def callback(self, interaction: discord.Interaction):
        if interaction.permissions.administrator:

            return
        await interaction.response.send_message(
            f"❌ You are not allowed to do this action!",
            ephemeral=True,
        )
