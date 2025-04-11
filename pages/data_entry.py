import streamlit as st
from sheets_connector import connect_to_sheets, append_score

st.set_page_config(page_title="🏁 Enter Score", layout="centered")

# Connect to Google Sheets
sheet = connect_to_sheets("gcp_service_account", "game_data")  

# Password Protection
st.title("🔐 Score Entry (Restricted)")
password = st.text_input("Enter password to proceed", type="password")

if password == "purustar":
    st.success("Access Granted. Please fill in the match details.")

    with st.form("score_form"):
        day = st.text_input("Match Day")
        game = st.text_input("Game ID/Name (e.g., 2)")
        a_score = st.text_input("Apoorv's Score")
        d_score = st.text_input("Darshan's Score")
        submitted = st.form_submit_button("Submit Score")

        if submitted:
            if not all([day, game, a_score, d_score]):
                st.warning("Please fill all fields.")
            else:
                row = [f"Day {day}", f"Game {game}", a_score, d_score]
                append_score(sheet, row)
                st.success("✅ Score successfully added to Google Sheets!")

else:
    st.warning("Enter password to view the score entry form.")