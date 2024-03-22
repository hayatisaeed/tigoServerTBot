from telegram.ext import ConversationHandler, MessageHandler, filters

import core.handlers.start_handler


async def function(update, context):
    pass


name = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^text$'),
                                     function)],
        states={
            "STATE": [
                MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),

                MessageHandler(filters.ALL, core.handlers.start_handler.return_home)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),
            MessageHandler(filters.COMMAND, core.handlers.start_handler.return_home)
        ]
    )