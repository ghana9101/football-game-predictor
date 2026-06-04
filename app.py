import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.set_page_config(page_title="Soccer 2026 Match Predictor", page_icon="⚽", layout="centered")

@st.cache_resource
def load_artifacts():
    model = joblib.load("models/match_predictor.pkl")
    team_data = joblib.load("models/team_data.pkl")
    team_stats = team_data["team_stats"]
    feature_cols = team_data["feature_cols"]
    return model, team_stats, feature_cols

model, team_stats, feature_cols = load_artifacts()

st.title("⚽ Soccer 2026 Match Predictor")
st.caption("Predictions based on historical international football results")

team_names = sorted(team_stats.keys())

col1, col2 = st.columns(2)
with col1:
    default_a = team_names.index("Brazil") if "Brazil" in team_names else 0
    team_a = st.selectbox("Team A", team_names, index=default_a)
with col2:
    default_b = team_names.index("Argentina") if "Argentina" in team_names else 1
    team_b = st.selectbox("Team B", team_names, index=default_b)

is_neutral = st.checkbox("Neutral venue", value=True)
is_major_tournament = st.checkbox("Major tournament (e.g. World Cup)", value=True)

if st.button("Predict", type="primary", use_container_width=True):
    if team_a == team_b:
        st.error("Please pick two different teams.")
    else:
        stats_a = team_stats[team_a]
        stats_b = team_stats[team_b]

        features = pd.DataFrame([{
            "team_a_winrate": stats_a["winrate"],
            "team_b_winrate": stats_b["winrate"],
            "team_a_goal_avg": stats_a["goal_avg"],
            "team_b_goal_avg": stats_b["goal_avg"],
            "team_a_recent_form": stats_a["recent_form"],
            "team_b_recent_form": stats_b["recent_form"],
            "is_neutral": int(is_neutral),
            "is_major_tournament": int(is_major_tournament)
        }])

        features = features[feature_cols]
        proba = model.predict_proba(features)[0]

        st.subheader("Match Outcome Probabilities")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"{team_a} wins", f"{proba[0]*100:.1f}%")
        with col2:
            st.metric("Draw", f"{proba[1]*100:.1f}%")
        with col3:
            st.metric(f"{team_b} wins", f"{proba[2]*100:.1f}%")

        st.progress(proba[0], text=f"{team_a} wins: {proba[0]*100:.1f}%")
        st.progress(proba[1], text=f"Draw: {proba[1]*100:.1f}%")
        st.progress(proba[2], text=f"{team_b} wins: {proba[2]*100:.1f}%")

        st.subheader("Team Statistics")
        stats_df = pd.DataFrame({
            "Team": [team_a, team_b],
            "Win Rate": [f"{stats_a['winrate']:.3f}", f"{stats_b['winrate']:.3f}"],
            "Avg Goals Scored": [f"{stats_a['goal_avg']:.2f}", f"{stats_b['goal_avg']:.2f}"],
            "Recent Form (Last 10)": [f"{stats_a['recent_form']:.3f}", f"{stats_b['recent_form']:.3f}"],
            "Matches Played": [stats_a["matches_played"], stats_b["matches_played"]]
        })
        st.table(stats_df)
