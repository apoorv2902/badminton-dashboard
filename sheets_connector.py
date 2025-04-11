import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect_to_sheets(json_keyfile_path, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1  # Or use get_worksheet(0)
    return sheet

def get_scores_df(sheet):
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def append_score(sheet, row):
    sheet.append_row(row)
