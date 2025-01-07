import discord

from app.db.database import SessionLocal
from app.db.models import Theme, User, VotedTheme
from app.utils import get_random_theme

from app.setup import bot

async def start_slaughter(user: discord.User) -> None:
    theme = get_random_theme(user.id)
    if theme is None:
        await user.send("No more themes to vote on.")
        return
    message = await user.send(f"Theme: {theme.theme}")
    await message.add_reaction("👍")
    await message.add_reaction("👎")
    
    try:
        reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == user and reaction.message == message)
    except Exception as e:
        print(e)
    else:
        await handle_slaughter_reaction(reaction, user)

async def handle_slaughter_reaction(reaction: discord.Reaction, user: discord.User) -> None:
    if reaction.message.author != bot.user:
        return
    session = SessionLocal()
    theme = session.query(Theme).filter(Theme.theme == reaction.message.content.split(": ")[1]).first()
    if not theme:
        return
    if str(reaction.emoji) == "👍":
        theme.likes += 1
    elif str(reaction.emoji) == "👎":
        theme.dislikes += 1
    voted_theme = VotedTheme(user_id=user.id, theme_id=theme.theme_id)
    session.add(voted_theme)
    session.commit()
    session.close()
    await reaction.message.delete()
    await start_slaughter(user)
