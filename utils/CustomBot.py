from __future__ import annotations

import logging
import traceback
from typing import List

import discord
import toml
from discord.ext import commands

intents = discord.Intents(
    messages=True,
    guilds=True,
    bans=True,
    emojis=True,
    typing=False, # we don't need typing.
    members=True, # Can turn this to true or false depending on if you want / have them
    presences=False # Same story as above
)

def get_pre(bot: CustomBot, message: discord.Message) -> List[str]:
    return commands.when_mentioned_or(bot.config["discord"]["prefix"])(bot, message)

class CustomBot(commands.Bot):
    def __init__(self, **options) -> None:
        super().__init__(command_prefix=get_pre, intents=intents, **options)

        self.config = toml.load("./config.toml")

        self._logger = logging.getLogger(__name__)
        
        self.load_extensions()

    def run(self, token: str = None, *, bot = True, reconnect = True) -> None:
        return super().run(token or self.config["discord"]["token"], bot=bot, reconnect=reconnect)

    def load_extensions(self):
        for extension in self.config["discord"]["extensions"]:
            try:
                self.load_extension(extension)
                self._logger.info(f"Loaded Extension {extension}")
            except Exception as e:
                self._logger.error(f"Failed to Load Extension {extension} \n {traceback.format_exc(e)}")                