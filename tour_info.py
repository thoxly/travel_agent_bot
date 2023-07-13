import pandas as pd
import numpy as np
import sqlite3
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters

TOUR_ID = 12  

def start_tour_info(update: Update, context: CallbackContext) -> int:
    if 'current_handler' in context.user_data and context.user_data['current_handler'] != 'tour_info':
        return ConversationHandler.END

    context.user_data['current_handler'] = 'tour_info'

    context.user_data.clear()
    context.chat_data.clear()
    text = "Введите номер телефона в формате (792*123123*)\n\n<code>❗Если вы наш постоянный клиент, то по номеру телефона мы покажем текущую (последнюю) заявку:</code>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    return TOUR_ID

def handle_tour_id(update: Update, context: CallbackContext) -> int:
    input_text = update.message.text

    # Connect to the SQLite database
    connection = sqlite3.connect('/root/database/tourbot.db')
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM data_tour WHERE phone_number = ?", (input_text,))
    row = cursor.fetchone()

    if row is None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка не найдена. Попробуйте ввести номер еще раз.")
        connection.close()
        return TOUR_ID
    else:
        addressing_name = row[4]
        date_start = row[10]
        number_of_nights = row[11]
        country = row[8]
        city = row[7]
        hotel = row[6]
        current_rate = row[19]
        to_be_pay_rur = row[17]

        text = f"Уважаемый(-ая), {addressing_name}!\n" \
               f"Дата начала вашего тура: {date_start}\n" \
               f"Количество ночей: {number_of_nights}\n" \
               f"Страна: {country}\n" \
               f"Город: {city}\n" \
               f"Название отеля: {hotel}\n" \
               f"По текущему курсу туроператора {current_rate} нужно доплатить: {to_be_pay_rur} руб.\n"

        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        connection.close()

        return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Вы вернулись в главное меню, выберите команду, нажав на синюю кнопку в левом нижнем углу")
    return ConversationHandler.END

def get_tour_info_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler('tour_info', start_tour_info)
        ],
        states={
            TOUR_ID: [
                MessageHandler(Filters.text & ~Filters.command, handle_tour_id)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True
    )
