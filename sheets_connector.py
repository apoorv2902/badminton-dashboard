import streamlit as st
import gspread
import json
import pandas as pd

def connect_to_sheets(secret_section_name: str, sheet_name: str):
    # Get credentials from secrets
    credentials_dict = json.loads(st.secrets[secret_section_name].to_json())

    # Authenticate with gspread using dict
    gc = gspread.service_account_from_dict(credentials_dict)

    # Open the sheet
    SHEET_ID = st.secrets["sheet_id"]
    sheet = gc.open_by_key(SHEET_ID).worksheet(sheet_name)

    return sheet

def get_scores_df(sheet):
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def append_score(sheet, row):
    sheet.append_row(row)
