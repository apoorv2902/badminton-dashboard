import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(page_title="📊 Dashboard", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, rgba(94, 42, 0, 0.9) 50%, rgba(0, 64, 128, 0.6) 100%);
        background-attachment: fixed;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)




brand_color = "#1f77b4"  # Main theme color
secondary_color = "#ff7f0e"  # Alternate for contrast

# Seaborn & Matplotlib tweaks

def set_dynamic_plot_style():
    import matplotlib as mpl
    theme = st.get_option("theme.base")
    is_dark = theme == "dark"
    bg = "#0e1117" if is_dark else "white"
    fg = "white" if is_dark else "black"
    grid = "#333" if is_dark else "#ddd"

    mpl.rcParams.update({
        "axes.facecolor": bg,
        "figure.facecolor": bg,
        "axes.edgecolor": fg,
        "axes.labelcolor": fg,
        "xtick.color": fg,
        "ytick.color": fg,
        "text.color": fg,
        "axes.titleweight": "bold",
        "grid.color": grid,
        "axes.grid": True,
        "grid.alpha": 0.3,
    })
    sns.set_style("darkgrid" if is_dark else "whitegrid")
    return bg, fg

# Then call it before plotting
bg_color, text_color = set_dynamic_plot_style()

# Load the data
from sheets_connector import connect_to_sheets, get_scores_df

# Connect to Google Sheet
try:
    sheet = connect_to_sheets("gcp_service_account", "game_data")
    df = get_scores_df(sheet)  
except Exception as e:
    st.error(f"❌ Could not connect to Google Sheets: {e}")
    st.stop()
# Fetch the data
df = get_scores_df(sheet)

# Clean scores
def to_score(val):
    return 20 if val == 'Deuce' else int(val)

df['A_score_num'] = df['A_score'].apply(to_score)
df['D_score_num'] = df['D_score'].apply(to_score)
df['Margin'] = abs(df['A_score_num'] - df['D_score_num'])
df['MarginCategory'] = df.apply(lambda row:
    'Deuce' if 'Deuce' in [str(row['A_score']), str(row['D_score'])] else
    'Close (<3)' if row['Margin'] is not None and row['Margin'] < 3 else
    'Normal', axis=1)
df['Winner'] = df.apply(lambda row: 'A' if row['A_score_num'] > row['D_score_num'] else 'D', axis=1)

df['GameIndex'] = range(1, len(df) + 1)
df['A_win'] = df['Winner'] == 'A'
df['D_win'] = df['Winner'] == 'D'
df['A_cum'] = df['A_win'].cumsum()
df['D_cum'] = df['D_win'].cumsum()
df['WinnerEncoded'] = df['Winner'].map({'A': 1, 'D': -1})
df['Streak'] = df['WinnerEncoded'].cumsum()

# Dashboard Title
st.title("🏸 Badminton Game Dashboard")

# Inline filter using columns
col1, col2 = st.columns([1, 5])  # col1 for dropdown, col2 for summary

with col1:
    player = st.selectbox("Player", ["Apoorv", "Darshan"], label_visibility="visible")

# Rest of the logic stays the same
key = 'A' if player == "Apoorv" else 'D'
score_col = 'A_score_num' if key == 'A' else 'D_score_num'
opponent_score_col = 'D_score_num' if key == 'A' else 'A_score_num'
cum_col = 'A_cum' if key == 'A' else 'D_cum'
color = brand_color if key == 'A' else secondary_color

selected_df = df[df['Winner'] == key]

# Calculate stats
player_stats = {
    'Total Wins': selected_df.shape[0],
    'Avg Score': df[score_col].mean(),
    'Avg Win Margin': selected_df['Margin'].mean(),
    'Deuce Wins': selected_df[((df['A_score'] == 'Deuce') | (df['D_score'] == 'Deuce'))].shape[0],
    'Close Wins': selected_df[selected_df['Margin'] < 3].shape[0],
    'Big Wins': selected_df[selected_df['Margin'] >= 5].shape[0],
}

# Show stats horizontally
with col2:
    st.header(f"📋 Summary for {player}")
    st.dataframe(pd.DataFrame([player_stats], index=[player]))


# --- Visuals ---


def apply_transparency(fig, ax, bg_color, alpha=0.5):
    fig.patch.set_facecolor(bg_color)
    fig.patch.set_alpha(alpha)
    ax.set_facecolor(bg_color)
    ax.patch.set_alpha(alpha)


# --- Overall Win & Games Per Day (Side-by-Side) ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🥇 Overall Win Percentage")
    winner_total = df['Winner'].value_counts()
    fig0, ax0 = plt.subplots(figsize=(4, 4))
    apply_transparency(fig0, ax0, bg_color)
    winner_total.plot(
        kind='pie',
        autopct='%1.1f%%',
        colors=[brand_color, secondary_color],
        ax=ax0,
        textprops={'color': text_color}
    )
    ax0.set_ylabel('')
    st.pyplot(fig0)

with col2:
    st.subheader("📅 Games Won Per Day")
    win_summary = df.groupby(['Day', 'Winner']).size().unstack(fill_value=0)
    fig1, ax1 = plt.subplots(figsize=(6, 4))  # slightly smaller for layout balance
    apply_transparency(fig1, ax1, bg_color)
    win_summary.plot(kind='bar', stacked=True, ax=ax1, color=[brand_color, "#ff7f0e"])
    ax1.set_ylabel("Wins")
    st.pyplot(fig1)


st.subheader(f"📊 Win Margin Distribution of {player}")
fig2, ax2 = plt.subplots(figsize=(10, 4))
apply_transparency(fig2, ax2, bg_color)
sns.histplot(selected_df['Margin'], bins=10, kde=True, ax=ax2, color=color)
ax2.set_title('Win Margin Distribution')
st.pyplot(fig2)

st.subheader("⚖️ Deuce vs Normal Games")
margin_counts = df['MarginCategory'].value_counts()
fig3, ax3 = plt.subplots(figsize=(10, 4))
apply_transparency(fig3, ax3, bg_color)
margin_counts.plot(kind='bar', ax=ax3, color=color)
ax3.set_ylabel("Count")
st.pyplot(fig3)

st.subheader("📈 Game-by-Game Scores Timeline (last 20)")
plot_df = df.dropna(subset=['A_score_num', 'D_score_num']).tail(20)
plot_df['Label'] = plot_df['Game'] + ' (' + plot_df['Day'] + ')'
fig4, ax4 = plt.subplots(figsize=(12, 5))
apply_transparency(fig4, ax4, bg_color)
ax4.plot(plot_df['Label'], plot_df['A_score_num'], marker='o', label='Apoorv (A)', color=brand_color)
ax4.plot(plot_df['Label'], plot_df['D_score_num'], marker='o', label='Darshan (D)', color='#ff7f0e')
ax4.set_ylabel('Score')
plt.xticks(rotation=45, ha='right')
ax4.set_title('Game-by-Game Scores')
ax4.legend()
st.pyplot(fig4)

st.subheader("📈 Cumulative Wins")
fig5, ax5 = plt.subplots()
apply_transparency(fig5, ax5, bg_color)
ax5.plot(df['GameIndex'], df['A_cum'], label='Apoorv (A)', marker='o', color=brand_color)
ax5.plot(df['GameIndex'], df['D_cum'], label='Darshan (D)', marker='o', color='#ff7f0e')
ax5.set_title('Cumulative Wins Over Games')
ax5.set_xlabel('Game #')
ax5.set_ylabel('Total Wins')
ax5.legend()
st.pyplot(fig5)

st.subheader("🔥 Game Streak Momentum")
fig6, ax6 = plt.subplots(figsize=(10, 5))
apply_transparency(fig6, ax6, bg_color)
ax6.step(df['GameIndex'], df['Streak'], where='mid', color=color)
ax6.axhline(0, color='gray', linestyle='--')
ax6.set_title('Momentum (+A / -D)')
ax6.set_xlabel('Game #')
ax6.set_ylabel('Streak Score')
st.pyplot(fig6)

st.subheader(f"🏆 Win Types by Margin of {player}")
category_win = selected_df.groupby('MarginCategory').size()
fig7, ax7 = plt.subplots(figsize=(10, 4))
apply_transparency(fig7, ax7, bg_color)
category_win.plot(kind='bar', ax=ax7, color=color)
ax7.set_ylabel("Win Count")
st.pyplot(fig7)


deuce_games = df[df['MarginCategory'] == 'Deuce']
deuce_wins = deuce_games['Winner'].value_counts()

daywise = df.pivot_table(index='Day', columns='Winner', values='Game', aggfunc='count').fillna(0)


col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Deuce Game Wins")
    fig8, ax8 = plt.subplots()
    apply_transparency(fig8, ax8, bg_color)
    deuce_wins.plot.pie(autopct='%1.1f%%', colors=[brand_color, "#ff7f0e"], ax=ax8)
    ax8.set_ylabel('')
    ax8.set_title('Deuce Game Wins')
    st.pyplot(fig8)

with col2:
    st.subheader("🌡️ Heatmap of Wins")
    fig9, ax9 = plt.subplots(figsize=(6,6 ))
    apply_transparency(fig9, ax9, bg_color)
    sns.heatmap(daywise, annot=True, fmt='g', cmap='mako_r', ax=ax9)
    st.pyplot(fig9)


