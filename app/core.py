import sys
from traceback import print_tb
from typing import cast

import discord

from app.setup import bot
from app.utils import try_dm


@bot.event
async def on_ready() -> None:
    print(f"Bot logged on as {bot.user}!")

@bot.event
async def on_error(*_: object) -> None:
    handle_error(cast(BaseException, sys.exc_info()[1]))

@bot.event
async def on_message(message: discord.Message) -> None:
    print(message)
    if message.author == bot.user:
        return

    if message.guild is None and message.content == "ping":
        await try_dm(message.author, "pong")
        return


def handle_error(error: BaseException) -> None:
    print(type(error).__name__, "->", error)
    print_tb(error.__traceback__)
    if isinstance(error, discord.app_commands.CommandInvokeError):
        handle_error(error.original)
