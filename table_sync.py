import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials
import time

# Путь к JSON-ключу сервисного аккаунта
json_keyfile_path = "creds.json"

# ID Google-таблицы
spreadsheet_id = "14rl2igwXTpJyJR14EQrfxZEtFepFxMkrzHVPCBzF4Yo"

# Функция для обновления локального файла
def update_local_file():
    # Авторизация и доступ к Google Sheets API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(credentials)

    # Открытие Google-таблицы
    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.worksheet("dataset")  # Замените на название нужного листа

    # Получение данных из Google-таблицы
    data = sheet.get_all_values()

    # Запись данных в файл CSV
    csv_file_path = "/root/vicbot/victory_tour/data_tour.csv"
    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

    # Вывод времени обновления
    print("Файл успешно обновлен. Время обновления:", time.ctime())

# Обновление файла с определенной периодичностью
while True:
    update_local_file()
    # Интервал обновления в секундах (например, каждые 4 часа = 4 * 60 * 60)
    time.sleep(4 * 60 * 60)
