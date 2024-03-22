from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

import core.config as config


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    args = context.args

    # check if user's information is saved
    user_data_is_saved = False  # *****
    if not user_data_is_saved:
        # check if started with a ref link
        if len(args) > 0 and not user_data_is_saved:
            possible_ref_id = args[0]
            ref_id_is_correct = False  # *****
            if ref_id_is_correct:
                ref_id = int(possible_ref_id)
            else:
                ref_id = 0
            username = ""  # *****
            name = ""  # *****

        pass  # save data in database etc # *****

    # make them join channel

    # separate admin and normal user
    if user_id != config.AdminData.adminChatId:  # normal user
        pass
    else:  # admin
        pass
