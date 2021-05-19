from __future__ import annotations

from discord.ext import commands
from utils import CustomBot

__all__ = ("BaseCog",)

class BaseCog(commands.Cog):
    __slots__ = "bot"

    def __init__(self, bot: CustomBot):
        self.bot = bot