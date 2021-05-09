from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

from utils import BaseCog, Codeblock
from discord.ext import commands

if TYPE_CHECKING:
    from utils.CustomBot import CustomBot

class OwnerCog(BaseCog, name="owner"):

    @commands.command(aliases = (
        "r",
    ))
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, cog: str):
        try:
            self.bot.reload_extension(cog)
            await ctx.send(f"Reloaded `{cog}`")
        except Exception as e:
            await ctx.reply(Codeblock(traceback.format_exc(e), lang="py"))

def setup(bot: CustomBot):
    bot.add_cog(OwnerCog(bot))
