from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import core.config as config
import core.handlers.start_handler
import core.utils.database_manager

conversation_handler_keyboard = [
    ['انصراف']
]
conversation_handler_markup = ReplyKeyboardMarkup(conversation_handler_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != config.AdminData.adminChatId:
        text = "You are not authorized to use this command."
        await context.bot.send_message(chat_id=user_id, text=text)
        await core.handlers.start_handler.return_home(update, context)
        return ConversationHandler.END

    broadcast_text = "پیام خود را بفرستید تا برای همه‌ی کاربران ارسال شود."
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=broadcast_text,
                                   reply_markup=conversation_handler_markup)
    return 'GET_MESSAGE'


async def get_message(update: Update, context: CallbackContext):
    message_id = update.effective_message.message_id
    users = core.utils.database_manager.get_all_user_ids()

    sent = 0
    failed = 0

    for user_id in users:
        try:
            await context.bot.copy_message(chat_id=user_id, from_chat_id=config.AdminData.adminChatId,
                                           message_id=message_id)
            sent += 1
        except:
            failed += 1

    text = f"""
    پیام با موفقیت ارسال شد
    
    تعداد ارسال موفق: {sent}
    تعداد خطا در ارسال: {failed}
    """
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text)
    await core.handlers.start_handler.return_home(update, context)
    return ConversationHandler.END
