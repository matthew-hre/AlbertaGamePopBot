import discord
from textwrap import shorten

Account = discord.User | discord.Member

async def try_dm(account: Account, content: str) -> None:
    if account.bot:
        return
    try:
        await account.send(content)
    except discord.Forbidden:
        print(f"Failed to DM {account} with: {shorten(content, width=50)}")
