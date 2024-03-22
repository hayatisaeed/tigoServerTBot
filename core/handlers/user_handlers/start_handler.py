from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext


user_start_reply_keyboard = []
user_start_reply_markup = ReplyKeyboardMarkup(user_start_reply_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    admin_start_test = "Hi!"
    await context.bot.send_message(chat_id=user_id, text=admin_start_test,
                                   reply_markup=user_start_reply_markup)
