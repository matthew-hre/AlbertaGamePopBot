from textwrap import shorten

import discord
from typing_extensions import TypeIs

import app.config as config

Account = discord.User | discord.Member


async def try_dm(account: Account, content: str) -> None:
    if account.bot:
        return
    try:
        await account.send(content)
    except discord.Forbidden:
        print(f"Failed to DM {account} with: {shorten(content, width=50)}")


def _has_role(member: discord.Member, role_id: int) -> bool:
    return member.get_role(int(role_id)) is not None


def is_dm(user: discord.User | discord.Member) -> TypeIs[discord.User]:
    return not isinstance(user, discord.Member)


def is_mod(member: discord.Member) -> bool:
    return _has_role(member, config.MOD_ROLE_ID)
