from __future__ import annotations

import logging
import traceback
import sys

import discord
import toml
from discord.ext import commands


class CustomBot(commands.AutoShardedBot):
    def __init__(self, **options) -> None:

        self.config = toml.load("./config.toml")

        super().__init__(
            command_prefix=commands.when_mentioned_or(self.config["bot"]["prefix"]),
            owner_ids = self.config["bot"]["owner_ids"], 
            intents= discord.Intents(
                messages=True,
                guilds=True,
                bans=True,
                emojis=True,
                typing=False, # we don't need typing.
                **self.config["bot"]["intents"]
                ), 
            allowed_mentions=discord.AllowedMentions(**self.config["bot"]["allowed_mentions"]),
            **options)

        self._init_logging()
        
        self._logger = logging.getLogger(__name__)
        
        self.load_extensions()

    def run(self, token: str = None, *, reconnect = True) -> None:
        return super().run(token or self.config["bot"]["token"], reconnect=reconnect)

    def load_extensions(self) -> None:
        for extension in self.config["bot"]["extensions"]:
            try:
                self.load_extension(extension)
                self._logger.info(f"Loaded Extension {extension}")
            except Exception as e:
                self._logger.error(f"Failed to Load Extension {extension} \n {''.join(traceback.format_tb(e.__traceback__))}")           

    async def on_error(self, event_method, *args, **kwargs) -> None:
        self._logger.error(f"An Error Occurred: {event_method}\n")
        _, _, trace = sys.exc_info()
        self._logger.error(''.join(traceback.format_tb(trace)))

    def _init_logging(self) -> None:
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, self.config["logging"]["level"]))
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(self.config["logging"]["format"]))     
        logger.addHandler(handler)