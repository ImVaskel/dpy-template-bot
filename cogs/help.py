from utils import CustomBot, CustomHelp
import discord
from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot: CustomBot) -> None:
        self.bot = bot
        self._original_help = bot.help_command
        bot.help_command = CustomHelp()
        bot.help_command.cog = self

    def cog_unload(self) -> None:
        self.bot.help_command = self._original_help
        

def setup(bot):
    bot.add_cog(HelpCog(bot))
