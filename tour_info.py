import pandas as pd
import numpy as np
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Poll
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters, CommandHandler
from telegram import ParseMode


TOUR_ID = 12  # Объявите TOUR_ID перед использованием

def start_tour_info(update: Update, context: CallbackContext) -> int:
    # прерываем текущий обработчик, если он существует
    if 'current_handler' in context.user_data and context.user_data['current_handler'] != 'tour_info':
        return ConversationHandler.END

    # устанавливаем текущий обработчик
    context.user_data['current_handler'] = 'tour_info'

    context.user_data.clear()
    context.chat_data.clear()
    text = "Введите номер телефона в формате (792*123123*)\n\n<code>❗Если вы наш постоянный клиент, то по номеру телефона мы покажем текущую (последнюю) заявку:</code>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)
    return TOUR_ID

def handle_tour_id(update: Update, context: CallbackContext) -> int:
    input_text = update.message.text
    df = pd.read_csv("/root/vicbot/victory_tour/data_tour.csv")

    df['phone_number'].replace('nan', np.nan, inplace=True)  # заменяем строки 'nan' на фактические NaN значения
    
    row = df[df['phone_number'].astype(str).str.contains(input_text)].tail(1)

    if row.empty:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ваша заявка не найдена. Попробуйте ввести номер еще раз.")
        return TOUR_ID  # возвращаемся в то же состояние, чтобы спросить номер тура снова
    else:
        text = f"Уважаемый(-ая), {row['addressing _name'].values[0]}!\n" \
               f"Дата начала вашего тура: {row['date_start'].values[0]}\n" \
               f"Количество ночей: {row['number_of_nights'].values[0]}\n" \
               f"Страна: {row['country'].values[0]}\n" \
               f"Город: {row['city'].values[0]}\n" \
               f"Название отеля: {row['hotel'].values[0]}\n" \
               f"По текущему курсу туроператора ({row['current_rate'].values[0]}) нужно доплатить: {row['to_be_pay_RUR'].values[0]} руб.\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)

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
