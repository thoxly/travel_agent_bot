import gspread
import sqlite3
from oauth2client.service_account import ServiceAccountCredentials
import time

# Путь к JSON-ключу сервисного аккаунта
json_keyfile_path = "creds.json"

# ID Google-таблицы
spreadsheet_id = "***************"

# Путь к файлу базы данных SQLite
db_file_path = "/root/database/tourbot.db"

# Функция для обновления базы данных SQLite
def update_database():
    # Авторизация и доступ к Google Sheets API
    scope = ["***************"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(credentials)

    # Открытие Google-таблицы
    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.worksheet("dataset")  # Замените на название нужного листа

    # Получение данных из Google-таблицы
    data = sheet.get_all_values()

    # Обновление базы данных SQLite
    connection = sqlite3.connect(db_file_path)
    cursor = connection.cursor()

    # Очистка существующих данных в таблице базы данных
    cursor.execute("DELETE FROM data_tour")

    # Вставка новых данных в таблицу базы данных
    for row in data:
        print(row)
        cursor.execute("INSERT INTO data_tour VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row[:-1])



    # Применение изменений и закрытие соединения с базой данных
    connection.commit()
    connection.close()

    # Вывод времени обновления
    print("База данных успешно обновлена. Время обновления:", time.ctime())

# Обновление базы данных каждый час
while True:
    update_database()
    # Интервал обновления в секундах (каждый час = 1 * 60 * 60)
    time.sleep(1 * 60 * 60)
