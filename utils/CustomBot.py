from __future__ import annotations

import logging
import traceback

import discord
import toml
from discord.ext import commands


class CustomBot(commands.Bot):
    def __init__(self, **options) -> None:

        self.config = toml.load("./config.toml")

        super().__init__(
            command_prefix=commands.when_mentioned_or(self.config["discord"]["prefix"]),
            owner_ids = self.config["discord"]["owner_ids"], 
            intents= discord.Intents(
                messages=True,
                guilds=True,
                bans=True,
                emojis=True,
                typing=False, # we don't need typing.
                members=self.config["discord"]["members_intent"], # Can turn this to true or false depending on if you want / have them
                presences=self.config["discord"]["presences_intent"] # Same story as above
                ), 
            **options)

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