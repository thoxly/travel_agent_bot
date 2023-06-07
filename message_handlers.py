from telegram import Update
from telegram.ext import CallbackContext
import re


def automatic_reply(update: Update, context: CallbackContext) -> None:
    message = update.message.text.lower()
    reply_text = get_cost_response(message)
    if reply_text:
        update.message.reply_text(reply_text)

def get_cost_response(message: str) -> str:
    if re.search(r"стоимость|цена|сколько стоит", message, re.IGNORECASE):
        return "Для расчета стоимости воспользуйтесь заполните заявку /tour_application"
    else:
        return "Я пока только учусь понимать человескую речь :)"