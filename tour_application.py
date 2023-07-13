import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
import emoji
from vicbot_calendar import create_calendar, inline_handler
from telegram import ParseMode
from datetime import datetime
from admin_utils import send_request_to_admin

NAME, PHONE, PHONE_WAITING, DEPARTURE, DESTINATION, DATES, DATES_SELECTED, NIGHTS, ADULTS, CHILDREN, CHILDREN_NUM, ADDITION_INFO = range(12)
   
def ask_for_name(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    context.chat_data.clear()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Как вас зовут?")
    return PHONE

def ask_for_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['name'] = update.message.text
    keyboard = [[KeyboardButton("Поделиться номером", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, поделитесь своим номером телефона или введите его вручную:", reply_markup=reply_markup)
    return PHONE_WAITING

def phone(update: Update, context: CallbackContext) -> int:
    phone_number = update.message.contact.phone_number if update.message.contact else update.message.text
    context.user_data['phone'] = phone_number
    update.message.reply_text(f"Ваш телефон {phone_number}", reply_markup=ReplyKeyboardRemove())
    return departure(update, context)

def departure(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    keyboard = [
        [InlineKeyboardButton("Москва", callback_data='moscow'), InlineKeyboardButton("Питер", callback_data='peter')],
        [InlineKeyboardButton("МинВоды", callback_data='mineral_waters'), InlineKeyboardButton("Уфа", callback_data='ufa')], 
        [InlineKeyboardButton("Казань", callback_data='kazan'), InlineKeyboardButton("Новосибирск", callback_data='novosib')],
        [InlineKeyboardButton("Cочи", callback_data='sochi'), InlineKeyboardButton("ЕКБ", callback_data='ekb')],
        [InlineKeyboardButton("Ставрополь", callback_data='stavropol'), InlineKeyboardButton("Н.Новгород", callback_data='nnov')],
        [InlineKeyboardButton("Круиз", callback_data='cruise'), InlineKeyboardButton("Без перелета", callback_data='no_fly')],
        
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="2️⃣ из 7️⃣ \n\nОткуда летим? ✈️", reply_markup=reply_markup)
    return DESTINATION

def destination(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    context.user_data['departure_city'] = query.data
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Турция 🇹🇷", callback_data='turkey'), InlineKeyboardButton("Египет 🇪🇬", callback_data='egypt'), InlineKeyboardButton("Мальдивы 🇲🇻", callback_data='maldives')],
        [InlineKeyboardButton("Сейшелы 🇸🇨", callback_data='seychelles'), InlineKeyboardButton("ОАЭ 🇦🇪", callback_data='uae'), InlineKeyboardButton("Тунис 🇹🇳", callback_data='tunisia')],
        [InlineKeyboardButton("Россия 🇷🇺", callback_data='russia'), InlineKeyboardButton("Кипр 🇨🇾", callback_data='cyprus'), InlineKeyboardButton("ЕС 🇪🇺", callback_data='eu')],
        [InlineKeyboardButton("Шри-Ланка 🇱🇰", callback_data='sri_lanka'), InlineKeyboardButton("Таиланд 🇹🇭", callback_data='thailand'), InlineKeyboardButton("Куба 🇨🇺", callback_data='cuba')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="3️⃣ из 7️⃣ \n\nГде будем отдыхать? ✈️ ", reply_markup=reply_markup)
    return DATES 

def dates(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    context.user_data['destination'] = query.data
    query.answer()
    now = datetime.now()
    reply_markup = create_calendar(now.year, now.month)
    context.bot.send_message(chat_id=update.effective_chat.id, text="4️⃣ из 7️⃣ \n\nВыберите предпочтительную дату вылета  📅", reply_markup=reply_markup)
    return DATES_SELECTED

def dates_selected(update: Update, context: CallbackContext) -> int:
    callback_data = update.callback_query.data.split(',')
    context.user_data['start_date'] = '/'.join(callback_data[1:])  # сохраняем выбранную дату
    update.callback_query.edit_message_text(text=f"Выбрана дата {context.user_data['start_date']}")
    # здесь вы можете продолжить вашу беседу или завершить ее
    context.bot.send_message(chat_id=update.effective_chat.id, text="5️⃣ из 7️⃣ \n\nОтлично! Укажите сколько ночей вы планируете остаться?")
    return NIGHTS

def nights(update: Update, context: CallbackContext) -> int:
    context.user_data['nights'] = update.message.text  # сохраняем количество ночей
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы выбрали {context.user_data['nights']} ночей.")
    
    keyboard = [
        [InlineKeyboardButton("👤", callback_data='1'), InlineKeyboardButton("👤👤", callback_data='2')],
        [InlineKeyboardButton("👤👤👤", callback_data='3'), InlineKeyboardButton("👤👤👤👤", callback_data='4')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="6️⃣ из 7️⃣ \n\nОтлично! Укажите количество взрослых туристов", reply_markup=reply_markup)
    return ADULTS

def adults(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.user_data['adults'] = query.data

    keyboard = [
        [InlineKeyboardButton("Да", callback_data='yes')],
        [InlineKeyboardButton("Еду без детей", callback_data='no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="7️⃣ из 7️⃣ \n\nСпасибо! А с вами едут дети?", reply_markup=reply_markup)
    return CHILDREN

def children(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    if query.data == 'no':
        context.user_data['children_num'] = '0'
        context.bot.send_message(chat_id=update.effective_chat.id, text="Дополнительная информация (необязательно); \nНапример, специальные требования к трансферу, конктреный отель, и т.д.")
        return ADDITION_INFO
    else:
        keyboard = [
            [InlineKeyboardButton("👦", callback_data='1'), InlineKeyboardButton("👦👧", callback_data='2')],
            [InlineKeyboardButton("👦👧👦", callback_data='3'), InlineKeyboardButton("👦👧👦👧", callback_data='4')],
            [InlineKeyboardButton("👦👧👦👧👦", callback_data='5')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=update.effective_chat.id, text="7️⃣ из 7️⃣ \n\nУкажите сколько детей", reply_markup=reply_markup)
        return CHILDREN_NUM

def children_num(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.user_data['children_num'] = query.data
    context.bot.send_message(chat_id=update.effective_chat.id, text="Дополнительная информация (необязательно);\nНапример, специальные требования к трансферу, конктреный отель, и т.д.\nЕсли нет, то введите 'нет'" )
    return ADDITION_INFO

def ask_addition_info(update: Update, context: CallbackContext) -> int:
    context.user_data['ask_addition_info'] = update.message.text
    send_request_to_admin(context, update.effective_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Супер! Вы стали ближе к путешествию✈️!\nВаша заявка на подбор тура отправлена 🔥 скоро с Вами свяжется наш менеджер.\n\nЯ умею много чего еще\nВернуться в главное меню /start")
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка на подбор тура была отменена.")
    return ConversationHandler.END

def get_tour_application_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('tour_application', ask_for_name)], 
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, ask_for_phone)],
            PHONE: [MessageHandler(Filters.text & ~Filters.command, ask_for_phone)],
            PHONE_WAITING: [MessageHandler(Filters.contact | Filters.text & ~Filters.command, phone)],
            DEPARTURE: [CallbackQueryHandler(departure)],
            DESTINATION: [CallbackQueryHandler(destination)],
            DATES: [CallbackQueryHandler(dates)],
            DATES_SELECTED: [CallbackQueryHandler(dates_selected, pattern='^calendar,'),
                            CallbackQueryHandler(inline_handler, pattern='^(previous-month|next-month)')],
            NIGHTS: [MessageHandler(Filters.text, nights)],
            ADULTS: [CallbackQueryHandler(adults)],
            CHILDREN: [CallbackQueryHandler(children)],
            CHILDREN_NUM: [CallbackQueryHandler(children_num)],
            ADDITION_INFO: [MessageHandler(Filters.text & ~Filters.command, ask_addition_info)],
        },

        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True     
    )


