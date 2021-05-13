from typing import Dict, List, Mapping, Optional, Tuple
from utils.CustomBot import CustomBot

import discord
from discord.ext import commands, menus
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command

__all__ = ("CustomHelp",)

class HelpPaginator(menus.MenuPages):
    def __init__(self, source, **kwargs):
        super().__init__(source, **kwargs)

class BotHelpSource(menus.ListPageSource):
    def __init__(self, entries, *, per_page=5):
        super().__init__(entries, per_page=per_page)

    async def format_page(self, menu: menus.Menu, entries: List[Tuple[Cog, List[Command]]]):

        embed = discord.Embed(
                color=menu.ctx.bot.color
            ).set_footer(
                text=f"Page {menu.current_page+1} / {self.get_max_pages()}"
            )
        
        for entry in entries:

            cog, commands = entry

            embed.add_field(
                name=cog.qualified_name, value = "".join(f" `{cmd.name}`" for cmd in commands)
            )

        return embed

class CustomHelp(commands.HelpCommand):
    def __init__(self, **options):

        attrs = {
            "hidden": True
        }

        super().__init__(command_attrs=attrs, **options)
    
    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command]]):

        commands_mapping: Dict[Cog, List[Command]] = {}

        for cog, commands in mapping.items():

            filtered = await self.filter_commands(commands)

            if filtered:
                commands_mapping[cog] = filtered

        # Convert to a list of `Tuple[Cog, Command]`
        commands = [
            (cog, commands) for cog, commands in commands_mapping.items()
        ]
            
        await HelpPaginator(BotHelpSource(commands, per_page=4)).start(self.context)
