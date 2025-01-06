import sys
from traceback import print_tb
from typing import cast

import discord
from discord.ext import commands

from app.db.database import init_db
from app.setup import bot
from app.utils import is_dm, is_mod, try_dm
from app.views import SuggestThemeView
from app.features.suggestions import list_all_suggestions

import app.config as config

init_db()


@bot.tree.command(name="suggest-theme", description="Suggest a theme for the game jam")
async def suggest_theme(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Click the button below to read the rules and suggest a theme.",
        view=SuggestThemeView(),
        ephemeral=True,
    )


@bot.tree.command(name="list-suggestions", description="List all theme suggestions")
@commands.has_role(int(config.MOD_ROLE_ID))
async def list_suggestions(interaction: discord.Interaction):
    response_message = await list_all_suggestions()
    await interaction.response.send_message(response_message, ephemeral=True)


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
    if is_dm(message.author):  # or not is_mod(message.author):
        return

    await bot.tree.sync()
    await try_dm(message.author, "Command tree synced.")


def handle_error(error: BaseException) -> None:
    print(type(error).__name__, "->", error)
    print_tb(error.__traceback__)
    if isinstance(error, discord.app_commands.CommandInvokeError):
        handle_error(error.original)
