import gspread
import os
from dotenv import load_dotenv
#gc = gspread.service_account_from_dict(credentials)
load_dotenv()  # Loads environment variables from .env file

creds_path = os.getenv("GOOGLE_CREDS_PATH")
gc = gspread.service_account(filename=creds_path)

sh = gc.open_by_key("1X_OgCH1dKqftUKEPXluDsUk6plmh8B0nvIkWyI-BiKs")

sh.sheet1.update_acell('B1', 'Biss!')

print(sh.sheet1.get('A1'))
