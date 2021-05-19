from __future__ import annotations

import logging
import os
import traceback
import sys

import discord
from discord.ext.commands.errors import ExtensionFailed
import toml
from discord.ext import commands

__all__ = ("CustomBot",)

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
                reactions=True,
                **self.config["bot"]["intents"]
                ), 
            allowed_mentions=discord.AllowedMentions(**self.config["bot"]["allowed_mentions"]),
            **options)

        self._init_logging()
        
        self._logger = logging.getLogger(__name__)
        
        self.color = self.config["bot"]["config"]["color"]
        self.error_color = self.config["bot"]["config"]["error_color"]

        self._set_env()
        self.load_extensions()

    def run(self, token: str = None, *, reconnect = True) -> None:
        return super().run(token or self.config["bot"]["token"], reconnect=reconnect)

    def load_extensions(self) -> None:
        for extension in self.config["bot"]["extensions"]:
            try:
                self.load_extension(extension)
                self._logger.info(f"Loaded Extension {extension}")
            except ExtensionFailed as e:
                self._logger.error(f"Failed to Load Extension {extension} \n {e}")

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

    def _set_env(self) -> None:
        """Sets the envs from the config"""
        for env, val in self.config["env"].items():
            os.environ[env] = val
