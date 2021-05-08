import logging
from utils.CustomBot import CustomBot

logger = logging.getLogger("root")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler() 
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if __name__ == "__main__":

    bot = CustomBot()

    try:
        bot.run()
    finally:
        bot._logger.info("Bot Closing")