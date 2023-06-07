import datetime
import time
import pandas as pd
import pytz
from telegram import Bot

def departure_notification():
    print("Notification function started")

    # Путь к вашему файлу
    csv_file_path = "/Users/glebperevalov/Desktop/Victory_tour/dataset.csv"  # Используйте ваш путь

    bot = Bot(token='6270034863:AAGE4WL6G92vwEalnRg_FoQFWYkZtURfyX4')

    moscow = pytz.timezone('Europe/Moscow')

    while True:
        now = datetime.datetime.now(moscow).replace(tzinfo=None)
        current_hour = now.hour

        if 9 <= current_hour < 21:
            df = pd.read_csv(csv_file_path)
            df['date_start'] = pd.to_datetime(df['date_start'], dayfirst=True)
            day_after_two_days = (now + datetime.timedelta(days=2)).replace(tzinfo=None)

            users_to_message = df[(df['date_start'] >= now) & (df['date_start'] <= day_after_two_days) & (df['message_sent'] == False)]  # замените 'message_sent' на название вашей колонки отслеживания отправки сообщений

            for index, user in users_to_message.iterrows():
                try:
                    bot.send_message(chat_id=user['user_id'], text='ПАКУЙ ЧЕМОДАН')  # замените 'user_id' на название вашей колонки с id пользователей
                    df.loc[index, 'message_sent'] = True
                    df.to_csv(csv_file_path, index=False)  # сохраняем обновленный файл csv
                except Exception as e:
                    print(f"Failed to send message to user {user['user_id']}. Error: {e}")

        time.sleep(600)

departure_notification()
