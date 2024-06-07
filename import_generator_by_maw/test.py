import gspread
def get_data_from_google_sheet():
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open("МАШ Сверка(продажа)")
    worksheet = sh.get_worksheet_by_id(986908701)
    values = worksheet.get_all_values()
    print(values)