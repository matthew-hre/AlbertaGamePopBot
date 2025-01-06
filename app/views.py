import discord
from app.features.suggestions import handle_theme_submission
from app.db.database import SessionLocal
from app.db.models import User

class SuggestThemeModal(discord.ui.Modal, title="Suggest a Theme"):
    theme = discord.ui.TextInput(
        label="Theme Suggestion",
        placeholder="Floating Islands",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True, thinking=True)
        response_message = await handle_theme_submission(interaction.user.id, self.theme.value)
        await interaction.edit_original_response(content=response_message)


class SuggestThemeView(discord.ui.View):
    @discord.ui.button(label="Accept Rules")
    async def read_rules(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        session = SessionLocal()
        user = session.query(User).filter(User.user_id == interaction.user.id).first()
        if not user:
            user = User(user_id=interaction.user.id, read_rules=True)
            session.add(user)
        else:
            user.read_rules = True
        session.commit()
        session.close()

        await interaction.response.send_modal(SuggestThemeModal())
