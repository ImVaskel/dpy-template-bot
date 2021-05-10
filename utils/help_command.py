import discord
from discord.ext import commands, menus

__all__ = ("CustomHelp",)

class HelpPaginator(menus.MenuPages):
    def __init__(self, source, **kwargs):
        super().__init__(source, **kwargs)

class CustomHelp(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
    
    async def send_bot_help(self, mapping):
        return await super().send_bot_help(mapping)