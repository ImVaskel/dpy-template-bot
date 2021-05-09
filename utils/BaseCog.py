from __future__ import annotations
from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from .CustomBot import CustomBot

__all__ = ("BaseCog",)

class BaseCog(commands.Cog):
    __slots__ = "bot"

    def __init__(self, bot: CustomBot):
        self.bot = bot