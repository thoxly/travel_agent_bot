import os
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, CallbackQueryHandler

COUNTRY_TOPIC = 1


def choosing_country(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    context.chat_data.clear()
    keyboard = [
        [InlineKeyboardButton("Турция 🇹🇷", callback_data='turkey'), InlineKeyboardButton("Египет 🇪🇬", callback_data='egypt'), InlineKeyboardButton("Мальдивы 🇲🇻", callback_data='maldives')],
        [InlineKeyboardButton("Сейшелы 🇸🇨", callback_data='seychelles'), InlineKeyboardButton("ОАЭ 🇦🇪", callback_data='uae'), InlineKeyboardButton("Тунис 🇹🇳", callback_data='tunisia')],
        [InlineKeyboardButton("Россия, Сочи 🇷🇺", callback_data='russia'), InlineKeyboardButton("Кипр 🇨🇾", callback_data='cyprus'), InlineKeyboardButton("ЕС 🇪🇺", callback_data='eu')],
        [InlineKeyboardButton("Шри-Ланка 🇱🇰", callback_data='sri_lanka'), InlineKeyboardButton("Таиланд 🇹🇭", callback_data='thailand'), InlineKeyboardButton("Куба 🇨🇺", callback_data='cuba')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите ваше направление', reply_markup=reply_markup)

    return COUNTRY_TOPIC

def country_topic(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    country = query.data

    document_path = f"/root/vicbot/victory_tour/memo/{country}.docx"

    if os.path.exists(document_path):
        # Отправляем документ пользователю
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(document_path, 'rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Документ готов к скачиванию! \n\nЯ умею много чего еще \nВернуться в главное меню /start")

    else:
        update.callback_query.message.reply_text("Документ не найден.")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    context.chat_data.clear()
    update.message.reply_text("Операция отменена. \nВернуться в главное меню /start")
    return ConversationHandler.END

def get_country_info_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler('memo', choosing_country)],
        states={
            COUNTRY_TOPIC: [CallbackQueryHandler(country_topic)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True        
    )
