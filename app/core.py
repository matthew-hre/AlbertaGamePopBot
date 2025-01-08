import sys
from traceback import print_tb
from typing import cast

import discord
from discord.ext import commands

import app.config as config
from app.db.database import SessionLocal, init_db
from app.db.models import Theme, User
from app.features.suggestions import list_all_suggestions
from app.setup import bot
from app.utils import is_dm, try_dm
from app.views import SlaughterRulesView, SuggestThemeModal, SuggestThemeView

init_db()


@bot.tree.command(name="suggest-theme", description="Suggest a theme for the game jam")
async def suggest_theme(interaction: discord.Interaction):
    async def get_suggest_theme_view(
        interaction: discord.Interaction,
    ) -> discord.ui.View | None:
        session = SessionLocal()
        user = session.query(User).filter(User.user_id == interaction.user.id).first()
        if not user:
            user = User(user_id=interaction.user.id, read_rules=True)
            session.add(user)
            session.commit()
            session.close()
            return SuggestThemeView()
        else:
            theme_count = (
                session.query(Theme).filter(Theme.user_id == user.user_id).count()
            )
            if theme_count >= 3:
                session.close()
                return None
            else:
                session.close()
                return SuggestThemeModal()

    view = await get_suggest_theme_view(interaction)
    if view is None:
        await interaction.response.send_message(
            "You have already suggested three themes.", ephemeral=True
        )
    elif isinstance(view, SuggestThemeView):
        await interaction.response.send_message(
            "Click the button below to read the rules and suggest a theme.",
            view=view,
            ephemeral=True,
        )
    else:
        await interaction.response.send_modal(SuggestThemeModal())


@bot.tree.command(name="list-suggestions", description="List all theme suggestions")
@commands.has_role(int(config.MOD_ROLE_ID))
async def list_suggestions(interaction: discord.Interaction):
    response_message = await list_all_suggestions()
    await interaction.response.send_message(response_message, ephemeral=True)


@bot.tree.command(name="delete-suggestion", description="Delete a theme suggestion")
@commands.has_role(int(config.MOD_ROLE_ID))
async def delete_suggestion(interaction: discord.Interaction, theme_id: int):
    session = SessionLocal()
    theme_id = int(interaction.data["options"][0]["value"])
    theme = session.query(Theme).filter(Theme.theme_id == theme_id).first()
    if not theme:
        response_message = f"Theme suggestion with ID {theme_id} not found."
    else:
        session.delete(theme)
        session.commit()
        response_message = f"Theme suggestion with ID {theme_id} deleted."
    session.close()
    await interaction.response.send_message(response_message, ephemeral=True)


@bot.tree.command(
    name="delete-all-suggestions", description="Delete all theme suggestions"
)
@commands.has_role(int(config.MOD_ROLE_ID))
async def delete_all_suggestions(interaction: discord.Interaction):
    session = SessionLocal()
    session.query(Theme).delete()
    session.commit()
    session.close()
    await interaction.response.send_message(
        "All theme suggestions deleted.", ephemeral=True
    )


@bot.tree.command(name="delete-user", description="Delete a user from the database")
@commands.has_role(int(config.MOD_ROLE_ID))
async def delete_user(interaction: discord.Interaction, who: discord.User):
    session = SessionLocal()
    user_id = who.id
    user = session.query(User).filter(User.user_id == user_id).first()
    if not user:
        response_message = f"User {user_id} not found."
    else:
        session.delete(user)
        session.commit()
        response_message = f"User {user_id} deleted."
    session.close()
    await interaction.response.send_message(response_message, ephemeral=True)


@bot.tree.command(name="slaughter", description="Begin the theme slaughter")
async def slaughter(interaction: discord.Interaction):
    dm_message = await try_dm(
        interaction.user,
        "Here are the rules of the theme slaughter. Please read and accept them to proceed.",
    )
    if dm_message:
        await dm_message.edit(view=SlaughterRulesView())
    await interaction.response.send_message(
        "Check your DMs for the slaughter rules.", ephemeral=True
    )


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
        print("Syncing command tree...")
        await sync(bot, message)


async def sync(bot: commands.Bot, message: discord.Message) -> None:
    """Syncs all global commands."""
    if is_dm(message.author):  # or not is_mod(message.author):
        return

    await bot.tree.sync()
    await try_dm(message.author, "Command tree synced.")


def handle_error(error: BaseException) -> None:
    print(type(error).__name__, "->", error)
    print_tb(error.__traceback__)
    if isinstance(error, discord.app_commands.CommandInvokeError):
        handle_error(error.original)
