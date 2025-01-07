from textwrap import shorten
import random

import discord
from typing_extensions import TypeIs

import app.config as config
from app.db.database import SessionLocal
from app.db.models import Theme, VotedTheme

Account = discord.User | discord.Member


async def try_dm(account: Account, content: str) -> discord.Message | None:
    if account.bot:
        return None
    try:
        return await account.send(content)
    except discord.Forbidden:
        print(f"Failed to DM {account} with: {shorten(content, width=50)}")
        return None


def _has_role(member: discord.Member, role_id: int) -> bool:
    return member.get_role(int(role_id)) is not None


def is_dm(user: discord.User | discord.Member) -> TypeIs[discord.User]:
    return not isinstance(user, discord.Member)


def is_mod(member: discord.Member) -> bool:
    return _has_role(member, config.MOD_ROLE_ID)


def get_random_theme(user_id: int) -> Theme | None:
    session = SessionLocal()
    voted_theme_ids = session.query(VotedTheme.theme_id).filter(VotedTheme.user_id == user_id).all()
    voted_theme_ids = [theme_id for (theme_id,) in voted_theme_ids]
    themes = session.query(Theme).filter(Theme.theme_id.notin_(voted_theme_ids)).all()
    if not themes:
        return None
    theme = random.choice(themes)
    session.close()
    return theme
