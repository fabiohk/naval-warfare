import logging
import logging.config
import os

from naval_warfare.game import prepare_game
from naval_warfare.game import show_final_boards
from naval_warfare.game import start

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "()": logging.Formatter,
                "format": "%(levelname)-8s [%(asctime)s] %(name)s: %(message)s",
            }
        },
        "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "standard"}},
        "loggers": {
            "": {"level": os.getenv("LOG_LEVEL", "WARNING"), "handlers": ["console"]},
        },
    }
)

if __name__ == "__main__":
    game = prepare_game()
    start(game)
    show_final_boards(game)
