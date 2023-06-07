from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import datetime
import calendar

def create_calendar(year, month):
    keyboard = []
    # Первая строка - месяц и год
    keyboard.append([InlineKeyboardButton(calendar.month_name[month] + " " + str(year), callback_data="ignore")])
    # Вторая строка - дни недели
    week_days = ["M", "T", "W", "T", "F", "S", "S"]
    row = []
    for day in week_days:
        row.append(InlineKeyboardButton(day, callback_data="ignore"))
    keyboard.append(row)

    # Дни месяца
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                row.append(InlineKeyboardButton(str(day), callback_data="calendar," + str(day) + "," + str(month) + "," + str(year)))
        keyboard.append(row)
    # Последняя строка - кнопки навигации
    keyboard.append([InlineKeyboardButton("<", callback_data="previous-month," + str(month) + "," + str(year)), 
                 InlineKeyboardButton(">", callback_data="next-month," + str(month) + "," + str(year))])
    return InlineKeyboardMarkup(keyboard)

def start(update: Update, context):
    now = datetime.datetime.now()
    context.bot.send_message(chat_id=update.message.chat_id, text="Here is the calendar:", reply_markup=create_calendar(int(now.year), int(now.month)))

def inline_handler(update: Update, context):
    try:
        callback_data = update.callback_query.data.split(',')
        if callback_data[0] == 'None':
            return
        elif 'next-month' in callback_data[0]:
            month = int(callback_data[1])
            year = int(callback_data[2])
            month += 1
            if month > 12:
                month = 1
                year += 1
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, 
                                          message_id=update.callback_query.message.message_id, 
                                          text="Please select a date: ", 
                                          reply_markup=create_calendar(year, month))
        elif 'previous-month' in callback_data[0]:
            month = int(callback_data[1])
            year = int(callback_data[2])
            month -= 1
            if month < 1:
                month = 12
                year -= 1
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id, 
                                          message_id=update.callback_query.message.message_id, 
                                          text="Please select a date: ", 
                                          reply_markup=create_calendar(year, month))
    except Exception as e:
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="Something went wrong.")


def main():
    updater = Updater(token='6270034863:AAGE4WL6G92vwEalnRg_FoQFWYkZtURfyX4', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(inline_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
