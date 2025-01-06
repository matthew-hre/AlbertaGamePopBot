import sys
from traceback import print_tb
from typing import cast

import discord
from discord.ext import commands

from app.db.database import SessionLocal, init_db
from app.db.models import Theme, User
from app.setup import bot
from app.utils import is_dm, is_mod, try_dm

init_db()


class SuggestThemeModal(discord.ui.Modal, title="Suggest a Theme"):
    theme = discord.ui.TextInput(
        label="Theme Suggestion",
        placeholder="Floating Islands",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True, thinking=True)
        session = SessionLocal()

        try:
            print(f"User ID: {interaction.user.id}")
            user = (
                session.query(User).filter(User.user_id == interaction.user.id).first()
            )
            if not user:
                print("User not found, creating new user.")
                user = User(user_id=interaction.user.id, read_rules=True)
                session.add(user)
                session.commit()

            print(f"Theme suggestion: {self.theme.value}")
            theme = Theme(user_id=user.user_id, theme=self.theme.value)
            session.add(theme)
            session.commit()

            await interaction.edit_original_response(
                content="Theme suggestion submitted!"
            )
        except Exception as e:
            print(f"An error occurred: {e}")
            await interaction.edit_original_response(content=f"An error occurred: {e}")
        finally:
            session.close()
            print("Session closed.")


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


@bot.tree.command(name="suggest-theme", description="Suggest a theme for the game jam")
async def suggest_theme(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Click the button below to read the rules and suggest a theme.",
        view=SuggestThemeView(),
        ephemeral=True,
    )


@bot.tree.command(name="list-suggestions", description="List all theme suggestions")
async def list_suggestions(interaction: discord.Interaction):
    session = SessionLocal()
    try:
        themes = session.query(Theme).all()
        if not themes:
            await interaction.response.send_message(
                "No theme suggestions found.", ephemeral=True
            )
            return

        suggestions = "\n".join(
            [
                f"{theme.theme_id}: {theme.theme} (by user {theme.user_id} at {theme.suggestion_time})"
                for theme in themes
            ]
        )
        await interaction.response.send_message(
            f"Theme Suggestions:\n{suggestions}", ephemeral=True
        )
    except Exception as e:
        await interaction.response.send_message(
            f"An error occurred: {e}", ephemeral=True
        )
    finally:
        session.close()


@bot.event
async def on_ready() -> None:
    print(f"Bot logged on as {bot.user}!")


@bot.event
async def on_error(*_: object) -> None:
    handle_error(cast(BaseException, sys.exc_info()[1]))


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author == bot.user:
        return

    if message.guild is None and message.content == "ping":
        await try_dm(message.author, "pong")
        return

    # mod-only sync command
    if message.content.rstrip() == "!sync":
        await sync(bot, message)


async def sync(bot: commands.Bot, message: discord.Message) -> None:
    """Syncs all global commands."""
    if is_dm(message.author) or not is_mod(message.author):
        return

    await bot.tree.sync()
    await try_dm(message.author, "Command tree synced.")


def handle_error(error: BaseException) -> None:
    print(type(error).__name__, "->", error)
    print_tb(error.__traceback__)
    if isinstance(error, discord.app_commands.CommandInvokeError):
        handle_error(error.original)
