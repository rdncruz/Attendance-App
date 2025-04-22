import gspread

gc = gspread.service_account(filename='../src/credentials.json')

sh = gc.open_by_key("1X_OgCH1dKqftUKEPXluDsUk6plmh8B0nvIkWyI-BiKs")

sh.sheet1.update_acell('B1', 'Biss!')

print(sh.sheet1.get('A1'))
