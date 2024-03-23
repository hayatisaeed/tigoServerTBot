from telegram import Update
from telegram.ext import CallbackContext
import core.utils.database_manager
import core.handlers.start_handler


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_data = core.utils.database_manager.get_user_data(user_id)
    user_is_blocked = core.utils.database_manager.user_is_blocked(user_id)
    text = f"""
            👤 اطلاعات این کاربر به شرح زیر است

            آیدی عددی:
            `{user_id}`

            💳 موجودی:
            `{user_data['credit']}` ریال

            📞 شماره تلفن:
            `{user_data['phone']}`

            🚔 وضعیت:
            `{'✅ verified' if user_data['verified'] else '❌ not verified'}`

            🪙 آیدی معرف:
            `{'None' if not user_data['ref'] else user_data['ref']}`

            💬 آیدی تلگرام:
            `{'@' + user_data['username'] if user_data['username'] != 'none' else 'None'}`

            {'🔴 این کاربر بلاک شده است'
    if user_is_blocked else ''}
            """
    await context.bot.send_message(chat_id=user_id, text=text)
    await core.handlers.start_handler.return_home(update, context)
