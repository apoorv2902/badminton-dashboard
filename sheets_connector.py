import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheets(secret_section_name: str, sheet_name: str):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # Load credentials from secrets
    credentials_dict = json.loads(st.secrets[secret_section_name])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

    # Authorize and connect
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1

    return sheet



def get_scores_df(sheet):
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def append_score(sheet, row):
    sheet.append_row(row)
