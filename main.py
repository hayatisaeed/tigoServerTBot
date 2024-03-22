# In the name of GOD

import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ConversationHandler
)

import core.config as config
import core.handlers.start_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    application = ApplicationBuilder().token(config.BotData.botFatherToken).build()

    # ------------ define handlers ------------ #

    # --- Command Handlers
    start_handler = CommandHandler('start', core.handlers.start_handler.handle)
    help_handler = CommandHandler('help', core.handlers.help_handler.handle)

    # --- Conversation Handlers

    # --- CallbackQuery Handlers

    # --- Message Handlers

    # ------------ end define handlers ------------ #

    # creating a list of handlers to add them easily
    handlers = [start_handler, help_handler]

    # Add Handlers To Application
    for handler in handlers:
        application.add_handler(handler)

    # Run Application Forever
    application.run_polling()


