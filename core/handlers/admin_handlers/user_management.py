from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import core.config as config
import core.handlers.start_handler
import core.utils.database_manager


user_management_keyboard = [
    ['لیست کاربران'],
    ['مدیریت کاربر'],
    ['انصراف']
]
user_management_markup = ReplyKeyboardMarkup(user_management_keyboard, one_time_keyboard=True, resize_keyboard=True)

cancel_markup = ReplyKeyboardMarkup([['انصراف']], one_time_keyboard=True, resize_keyboard=True)

manage_user_keyboard = [
    ['ویرایش موجودی'],
    ['پیام به کاربر'],
    ['block / unblock'],
    ['انصراف']
]
manage_user_markup = ReplyKeyboardMarkup(manage_user_keyboard, one_time_keyboard=True, resize_keyboard=True)


async def handle(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != config.AdminData.adminChatId:
        text = "You are not authorized to use this command."
        await context.bot.send_message(chat_id=user_id, text=text)
        await core.handlers.start_handler.return_home(update, context)
        return ConversationHandler.END

    text = "👤 مدیریت کاربران"
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text, reply_markup=user_management_markup)
    return 'CHOOSING'


async def list_of_users(update: Update, context: CallbackContext):
    users = core.utils.database_manager.get_all_user_ids()
    text = """
    لیست کاربران حاضر در بات:
    
    
    """
    for user_id in users:
        text += f" `{user_id}`  "

    text += """
    برای مدیریت هر کاربر، در بخش مدیریت کاربر، آیدی عددی او را ارسال کنید.
    """
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text, reply_markup=user_management_markup)
    return 'CHOOSING'


async def manage_user(update: Update, context: CallbackContext):
    text = """
    لطفا آیدی عددی کاربر مدنظر رو ارسال کنید
    """
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text, reply_markup=cancel_markup)
    return 'GET_USER_ID'


async def get_user_id(update: Update, context: CallbackContext):
    user_id = update.message.text
    try:
        user_id = int(user_id)
        user_exists = core.utils.database_manager.user_exists(user_id)
    except:
        user_exists = False

    if not user_exists:
        text = """
        کاربر یافت نشد. لطفا آیدی عددی را دوباره وارد نمایید
        """
        await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text, reply_markup=cancel_markup)
        return 'GET_USER_ID'
    else:
        context.user_data['current_user'] = user_id
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
        await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text)
        text2 = """
        برای مدیریت کاربر لطفا یکی از دکمه‌های زیر را بزنید
        """
        await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text2, reply_markup=manage_user_markup)
        return 'CHOOSING_MANAGE_USER'


async def change_credit(update: Update, context: CallbackContext):
    pass


async def change_credit_get_number(update: Update, context: CallbackContext):
    pass


async def send_message_to_user(update: Update, context: CallbackContext):
    user_id = context.user_data['current_user']
    user_id = int(user_id)
    user_data = core.utils.database_manager.get_user_data(user_id)

    text = """
    شما در حال ارسال پیام به کاربر با مشخصات زیر میباشید:
    id: {user_id}
    username: @{user_data['username']}
    
    لطفا پیام خود را ارسال کنید
    """
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text, reply_markup=cancel_markup)
    return 'GET_MESSAGE'


async def send_message_to_user_get_message(update: Update, context: CallbackContext):
    user_id = context.user_data['current_user']

    await context.bot.copy_message(chat_id=user_id, from_chat_id=config.AdminData.adminChatId,
                                   message_id=update.message.message_id)
    text = """
    پیام با موفقیت ارسال شد.
    """
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text, reply_markup=manage_user_markup)
    return 'CHOOSING_MANAGE_USER'


async def block_unblock_user(update: Update, context: CallbackContext):
    user_id = context.user_data['current_user']
    user_is_blocked = core.utils.database_manager.user_is_blocked(user_id)

    text = f"""
     🆔 آیدی عددی:
    `{user_id}`
            
    {
    '🟢 این کاربر از لیست بلاک شده ها خارج شد'
        if user_is_blocked else
        '🔴 این کاربر بلاک شد.'
    }
    """
    core.utils.database_manager.block_unblock_user(user_id)  # saving to database
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text)

    if user_is_blocked:
        text = """
        ✅ شما از لیست بلاک شده‌ها خارج شدید و هم اکنون میتوانید از بات استفاده کنید.
        برای استفاده‌ی مجدد دستور زیر را بزنید
        
        /start
        """
    else:
        text = """
        🔴 دسترسی شما به بات از طرف مدیریت محدود شد.
        """
    await context.bot.send_message(chat_id=user_id, text=text)

    text = """
    از منوی زیر انتخاب کنید
    """
    await context.bot.send_message(chat_id=config.AdminData.adminChatId, text=text, reply_markup=manage_user_markup)
    return 'CHOOSING_MANAGE_USER'
