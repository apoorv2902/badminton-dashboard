import streamlit as st

st.set_page_config(
    page_title="Badminton Tracker",
    page_icon="🏸",
    layout="centered"
)

st.title("🏸 Welcome to the Badminton Analytics App")

st.markdown("""
Welcome to **Badminton Tracker Dashboard**.  
Use the sidebar to:

- 📊 View **Dashboard** of past games
- 🏁 Enter new **Game Scores** (password-protected)

""")
