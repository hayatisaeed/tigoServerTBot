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
import core.handlers.help_handler
import core.handlers.admin_handlers.user_management
import core.handlers.user_handlers.profile_handler

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

    admin_user_management_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^کاربران$'),
                                     core.handlers.admin_handlers.user_management.handle)],
        states={
            "CHOOSING": [
                MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),
                MessageHandler(filters.Regex('^لیست کاربران$'),
                               core.handlers.admin_handlers.user_management.list_of_users),
                MessageHandler(filters.Regex('^مدیریت کاربر$'),
                               core.handlers.admin_handlers.user_management.manage_user),
                MessageHandler(filters.ALL, core.handlers.start_handler.return_home)
            ],
            "GET_USER_ID": [
                MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.admin_handlers.user_management.get_user_id),
                MessageHandler(filters.ALL, core.handlers.start_handler.return_home)
            ],
            "GET_NEW_CREDIT": [
                MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),
                MessageHandler(filters.TEXT, core.handlers.admin_handlers.user_management.change_credit_get_number),
                MessageHandler(filters.ALL, core.handlers.start_handler.return_home)
            ],
            'CHOOSING_MANAGE_USER': [
                MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),
                MessageHandler(filters.Regex('^block / unblock$'),
                               core.handlers.admin_handlers.user_management.block_unblock_user),
                MessageHandler(filters.Regex('^پیام به کاربر$'),
                               core.handlers.admin_handlers.user_management.send_message_to_user),
                MessageHandler(filters.Regex('^ویرایش موجودی$'),
                               core.handlers.admin_handlers.user_management.change_credit),
                MessageHandler(filters.ALL, core.handlers.start_handler.return_home)
            ],
            'GET_MESSAGE': [
                MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),
                MessageHandler(filters.ALL,
                               core.handlers.admin_handlers.user_management.send_message_to_user_get_message)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex('^انصراف$'), core.handlers.start_handler.return_home),
            MessageHandler(filters.COMMAND, core.handlers.start_handler.return_home)
        ]
    )

    # --- CallbackQuery Handlers

    # --- Message Handlers

    user_profile_handler = MessageHandler(filters.Regex('^پروفایل کاربری$'),
                                          core.handlers.user_handlers.profile_handler.handle)

    # ------------ end define handlers ------------ #

    # creating a list of handlers to add them easily
    handlers = [
        start_handler, help_handler, admin_broadcast_conv_handler, admin_user_management_conv_handler,
        user_profile_handler
    ]

    # Add Handlers To Application
    for handler in handlers:
        application.add_handler(handler)

    # Run Application Forever
    application.run_polling()


if __name__ == '__main__':
    print('- [ Bot Started ] -')
    main()
