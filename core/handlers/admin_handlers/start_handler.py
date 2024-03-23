from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
import core.config as config


admin_start_reply_keyboard = [
    ['پیام همگانی', 'کاربران'],
    ['درگاه پرداخت']
]
admin_start_reply_markup = ReplyKeyboardMarkup(admin_start_reply_keyboard, one_time_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    admin_start_test = "Hi!"
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=admin_start_test,
                                   reply_markup=admin_start_reply_markup)
