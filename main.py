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
import core.handlers.admin_handlers.broadcast_handler

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
    admin_broadcast_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^پیام همگانی$'),
                                     core.handlers.admin_handlers.broadcast_handler.handle)],
        states={
            "GET_MESSAGE": [
                MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),
                MessageHandler(filters.ALL, core.handlers.admin_handlers.broadcast_handler.get_message)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),
            MessageHandler(filters.COMMAND, core.handlers.start_handler.return_home)
        ]
    )

    # --- CallbackQuery Handlers

    # --- Message Handlers

    # ------------ end define handlers ------------ #

    # creating a list of handlers to add them easily
    handlers = [start_handler, help_handler, admin_broadcast_conv_handler]

    # Add Handlers To Application
    for handler in handlers:
        application.add_handler(handler)

    # Run Application Forever
    application.run_polling()


if __name__ == '__main__':
    print('- [ Bot Started ] -')
    main()
