import discord

from app.features.slaughter import start_slaughter
from app.features.suggestions import handle_theme_submission


class SuggestThemeModal(discord.ui.Modal, title="Suggest a Theme"):
    theme = discord.ui.TextInput(
        label="Theme Suggestion",
        placeholder="Floating Islands",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True, thinking=True)
        response_message = await handle_theme_submission(
            interaction.user.id, self.theme.value
        )
        await interaction.edit_original_response(content=response_message)


class SuggestThemeView(discord.ui.View):
    @discord.ui.button(label="Accept Rules")
    async def read_rules(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(SuggestThemeModal())


class SlaughterRulesView(discord.ui.View):
    @discord.ui.button(label="Accept Rules")
    async def accept_rules(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.edit_message(
            content="You have accepted the rules. Starting slaughter...", view=None
        )
        await start_slaughter(interaction.user)
