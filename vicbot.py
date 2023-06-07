import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from tour_info import get_tour_info_conversation_handler, start_tour_info
from tour_application import get_tour_application_conversation_handler, ask_for_name
from victorina import victorina_conv_handler
from country_info import get_country_info_handler, choosing_country
from message_handlers import automatic_reply
import csv
from datetime import datetime

user_data = {}

def log_user_interaction(user_id, command):
    with open('user_interaction.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([user_id, command, datetime.now()])

def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = user.id
    context.user_data.clear()
    context.chat_data.clear()
    log_user_interaction(user_id, "start")  # log this interaction
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
    Здравствуйте! Чем могу помочь?

/tour_application - заявка на подбор тура 📍

/tour_info - о моем туре ℹ️

/memo - памятка 📑

/victorina - викторина 🧠 

/cancel - отмена ↩️

""")

logging.basicConfig(level=logging.INFO)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
    
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_id = user.id
    context.user_data.clear()
    context.chat_data.clear()
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
    updater = Updater("6270034863:AAGE4WL6G92vwEalnRg_FoQFWYkZtURfyX4")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(get_tour_application_conversation_handler())
    dispatcher.add_handler(get_tour_info_conversation_handler())
    dispatcher.add_handler(get_country_info_handler())
    dispatcher.add_handler(victorina_conv_handler())
    dispatcher.add_handler(CommandHandler('cancel', cancel))
    dispatcher.add_handler(MessageHandler(Filters.text, automatic_reply))
    #dispatcher.add_handler(CommandHandler('tour_application', ask_for_name))
    #dispatcher.add_handler(CommandHandler('tour_info', start_tour_info))
    #dispatcher.add_handler(CommandHandler('memo', choosing_country))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
