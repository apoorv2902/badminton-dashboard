import os
import json

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd

def connect_to_sheets(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    service_account_info = json.loads(os.environ["gcp_service_account"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1
    return sheet

def get_scores_df(sheet):
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def append_score(sheet, row):
    sheet.append_row(row)
