import traceback
import logging
from typing import TYPE_CHECKING, Tuple

from discord.ext.commands.errors import CommandError
from utils.CustomBot import CustomBot
from utils.BaseCog import BaseCog

import discord
from discord.ext import commands

from utils.models import Codeblock

class ErrorHandler(BaseCog):
    __slots__ = ("bot", "ignored_errors", "_logger")

    if TYPE_CHECKING:
        bot: CustomBot
        ignored_errors: Tuple[Exception]
        _logger: logging.Logger

    def __init__(self, bot: CustomBot):
        super().__init__(bot)
        self.ignored_errors = (commands.CommandNotFound, )
        self._logger = logging.getLogger(__name__)  

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: CommandError):
        error = getattr(error, "original", error) # Unpack the error

        if isinstance(error, self.ignored_errors):
            return

        if isinstance(error, CommandError):
            embed = discord.Embed(description=str(error))
            await ctx.reply(embed=embed)

        else:
            embed = discord.Embed(description=Codeblock(str(error), lang="py"))
            await ctx.reply(embed=embed)
            self._logger.error(''.join(traceback.format_tb(error.__traceback__)))
            

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
