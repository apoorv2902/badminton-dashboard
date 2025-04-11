import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheets(secret_section_name: str, sheet_name: str):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # Convert secrets AttrDict to a regular dict for gspread
    credentials_dict = dict(st.secrets[secret_section_name])

    # Create credentials and authorize gspread
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scopes=scope)
    gc = gspread.authorize(creds)

    # Use Sheet ID from secrets
    sheet_id = credentials_dict["sheet_id"]  
    sheet = gc.open_by_key(sheet_id).worksheet(sheet_name)

    return sheet

def get_scores_df(sheet):
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def append_score(sheet, row):
    sheet.append_row(row)
