from __future__ import annotations

from typing import Optional

import discord
from discord.ext.commands.errors import ExtensionError
from utils import BaseCog, Codeblock, CustomBot
from discord.ext import commands 

class CleanupFlags(commands.FlagConverter):
    num: Optional[int] = 5
    bulk: Optional[bool] = False

class OwnerCog(BaseCog, name="owner"):

    @commands.is_owner()
    @commands.group(name="dev")
    async def dev_group(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @dev_group.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, cog: str):
        try:
            self.bot.reload_extension(cog)
            await ctx.send(f"Reloaded `{cog}`")
        except ExtensionError as e:
            await ctx.reply(Codeblock(str(e), lang="py"))

    @dev_group.command()
    @commands.is_owner()
    async def cleanup(self, ctx: commands.Context, *, flags: CleanupFlags):
        num = len(await ctx.channel.purge(limit = flags.num, check = lambda m: m == self.bot.user, bulk = flags.bulk))
        await ctx.reply(
            embed = discord.Embed(description=f"\N{THUMBS UP SIGN} Successfully deleted {num}/{flags.num} messages.", color=self.bot.color), 
            delete_after=25
        )

    @dev_group.command()
    @commands.is_owner()
    async def delete(self, ctx: commands.Context, message: discord.PartialMessage = None):
        """
        Deletes the given message, can also be a reply.
        """
        if message is None:
            if ctx.message.reference:
                message = ctx.message.reference.cached_message
            else:
                raise commands.BadArgument("No message given.")
        
        try:
            await message.delete()
            await ctx.message.add_reaction("\N{THUMBS UP SIGN}")
        except Exception as error:
            embed = discord.Embed(description=Codeblock(str(error), lang="py"), color=self.bot.error_color)
            await ctx.reply(embed=embed)

def setup(bot: CustomBot):
    bot.add_cog(OwnerCog(bot))
