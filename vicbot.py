import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from tour_info import get_tour_info_conversation_handler, start_tour_info
from tour_application import get_tour_application_conversation_handler, ask_for_name
from victorina import victorina_conv_handler
from country_info import get_country_info_handler, choosing_country
from message_handlers import automatic_reply
from datetime import datetime
import sqlite3

def add_bot_id(user_id, bot_id, conn):
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM bots WHERE ID = ?', (user_id,))
    data = cursor.fetchone()
    if data is not None:
        # Если запись существует, обновляем значение bot_id
        cursor.execute('UPDATE bots SET bot_id = ? WHERE ID = ?', (bot_id, user_id))
    else:
        # Если записи нет, выполняем вставку новой записи
        cursor.execute('INSERT INTO bots (ID, bot_id) VALUES (?, ?)', (user_id, bot_id))
    
    conn.commit()
    cursor.close()

def log_user_interaction(user_id, command, conn, bot_id):
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    cursor.execute('INSERT INTO user_interaction (bot_id, user_id, command, datetime) VALUES (?, ?, ?, ?)', (bot_id, user_id, command, timestamp))
    conn.commit()
    
    cursor.close()

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = user.id
    bot_id = context.bot.id
    conn = sqlite3.connect('/root/database/tourbot.db')
    cursor = conn.cursor()
    log_user_interaction(user_id, "start", conn, bot_id)
    add_bot_id(user_id, bot_id, conn)
    conn.close()

    context.bot.send_message(chat_id=update.effective_chat.id, text="""
    Здравствуйте! Чем могу помочь?

/tour_application - заявка на подбор тура 📍

/tour_info - о моем туре ℹ️

/memo - памятка 📑

/victorina - викторина 🧠 

/cancel - отмена ↩️

""")

def cancel(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    context.chat_data.clear()
    update.message.reply_text("Операция отменена. Вы вернулись в основное меню.")
    return ConversationHandler.END

def main() -> None:
    updater = Updater("************************")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(get_tour_application_conversation_handler())
    dispatcher.add_handler(get_tour_info_conversation_handler())
    dispatcher.add_handler(get_country_info_handler())
    dispatcher.add_handler(victorina_conv_handler())
    dispatcher.add_handler(CommandHandler('cancel', cancel))
    dispatcher.add_handler(MessageHandler(Filters.text, automatic_reply))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

