import sqlite3
from telegram.ext import CallbackContext

def save_request_to_income_app(context: CallbackContext) -> None:
    conn = sqlite3.connect("/root/databse/tourbot.db")  # Замените "your_database.db" на имя вашей базы данных SQLite
    cursor = conn.cursor()

    # Получите данные из контекста
    phone = context.user_data['phone']
    name = context.user_data['name']
    departure_city = context.user_data['departure_city']
    destination = context.user_data['destination']
    start_date = context.user_data['start_date']
    nights = context.user_data['nights']
    adults = context.user_data['adults']
    children_num = context.user_data.get('children_num', 0)
    ask_addition_info = context.user_data['ask_addition_info']

    # Выполните SQL-запрос для вставки данных в таблицу income_app
    cursor.execute("INSERT INTO income_app (phone, name, departure_city, destination, start_date, nights, adults, children_num, ask_addition_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (phone, name, departure_city, destination, start_date, nights, adults, children_num, ask_addition_info))

    # Сохраните изменения в базе данных
    conn.commit()

    # Закройте соединение с базой данных
    cursor.close()
    conn.close()

def send_request_to_admin(context: CallbackContext, user_id: int) -> None:
    request_info = (
        f"Новая заявка от пользователя с ID {user_id}: \
            \nТелефон: {context.user_data['phone']} \
            \nИмя:{context.user_data['name']}\
            \nВылет из:{context.user_data['departure_city']} \
            \nНаправление:{context.user_data['destination']} \
            \n \
            \nДата вылета(ДД-ММ-ГГГГ): {context.user_data['start_date']}\
            \nКоличество ночей: {context.user_data['nights']}\
            \nКоличество взрослых: {context.user_data['adults']}   \
            \nКоличество детей: {context.user_data.get('children_num', '0')} \
            \nДопы: {context.user_data['ask_addition_info']} "
            )
    context.bot.send_message(chat_id=298161005, text=request_info)
    context.bot.send_message(chat_id=1181501430, text=request_info)

    # Сохраните заявку в таблицу income_app
    save_request_to_income_app(context)
        
