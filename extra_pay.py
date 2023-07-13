import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_extra_pay(tour_id):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)

    # Открываем google sheet по имени
    sheet = client.open("data_tour").worksheet("dataset")  # Используйте ваше название

    # Получаем все значения из столбца 'A'
    tour_ids = sheet.col_values(1) 

    # Проверяем наличие tour_id в столбце 'A'
    if tour_id in tour_ids:
        # Если tour_id найден, получаем соответствующее значение из столбца 'K'
        row = tour_ids.index(tour_id) + 1
        extra_pay = sheet.cell(row, 12).value  # 11 потому что K - 11й столбец
        return f'К оплате {extra_pay} руб.'
    else:
        return 'ID tour не найден'
