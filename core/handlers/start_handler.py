from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

import core.config as config
import core.utils.database_manager
import core.handlers.admin_handlers.start_handler
import core.handlers.user_handlers.start_handler


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    args = context.args

    # check if user's information is saved
    user_data_is_saved = core.utils.database_manager.user_exists(int(user_id))
    if not user_data_is_saved:
        # check if started with a ref link
        ref = 0
        if len(args) > 0 and not user_data_is_saved:
            possible_ref_id = args[0]
            try:
                possible_ref_id = int(possible_ref_id)
                ref_id_is_correct = core.utils.database_manager.user_exists(possible_ref_id)
            except ValueError:
                ref_id_is_correct = False

            if ref_id_is_correct:
                ref = int(possible_ref_id)

        username = update.effective_user.username
        username = username if username else "none"  # if username does not exist, saves none instead
        phone = "0"
        credit = 0.0

        core.utils.database_manager.create_user(user_id, username, phone, credit, ref=ref)

    # make them join channel

    # separate admin and normal user
    if user_id != config.AdminData.adminChatId:  # normal user
        await core.handlers.user_handlers.start_handler.handle(update, context)
    else:  # admin
        await core.handlers.admin_handlers.start_handler.handle(update, context)


async def return_home(update: Update, context: CallbackContext):
    await handle(update, context)
    return ConversationHandler.END
