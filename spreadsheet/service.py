import os
from dotenv import load_dotenv
import gspread
from gspread.exceptions import WorksheetNotFound
from google.oauth2.service_account import Credentials

load_dotenv()

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    './credentials.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)
sh = gc.open_by_key(SPREADSHEET_ID)

def get_worksheet(name): 
    try:
        worksheet = sh.worksheet(name)
        return worksheet
    except WorksheetNotFound:
        print("Worksheet not found. Creating one worksheet")
        return create_worksheet(name)

def create_worksheet(name):
    worksheet = sh.add_worksheet(title=name,rows=100, cols=50)
    worksheet.append_row(['Id','Username','Name','Room Number','Position'])
    worksheet.format('A1:E1',{"textFormat": {"bold": True}})
    worksheet.freeze(rows=1, cols=None)
    return worksheet
