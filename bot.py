import logging
from utils.CustomBot import CustomBot

if __name__ == "__main__":

    bot = CustomBot()

    try:
        bot.run()
    finally:
        bot._logger.info("Bot Closing")