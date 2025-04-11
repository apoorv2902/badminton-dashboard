import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="🏁 Enter Score", layout="centered")

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
                new_data = pd.DataFrame([{
                    "Day": f"Day {day}",
                    "Game": f"Game {game}",
                    "A_score": a_score,
                    "D_score": d_score
                }])
                
                filepath = "data/game_data.csv"
                if os.path.exists(filepath):
                    df = pd.read_csv(filepath)
                    df = pd.concat([df, new_data], ignore_index=True)
                else:
                    df = new_data

                df.to_csv(filepath, index=False)
                st.success("Score successfully added!")

else:
    st.warning("Enter password to view the score entry form.")

