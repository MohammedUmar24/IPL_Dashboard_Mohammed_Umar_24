import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="IPL Dashboard", layout="wide")

st.title("🏏 IPL Cricket Data Dashboard")
st.markdown("Explore IPL matches, teams, players, and more!")

# Load Data
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries_url = "https://drive.google.com/file/d/10JDHJf28LAGnZ8REPQ5buNjQrpx1mu9n/view?usp=drive_link"
    deliveries = pd.read_csv(deliveries_url)
    return matches, deliveries

matches, deliveries = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
season = st.sidebar.selectbox("Select Season", sorted(matches['season'].unique(), reverse=True))
team = st.sidebar.selectbox("Select Team", sorted(matches['winner'].dropna().unique()))

# Season and Team Analysis
st.subheader(f"📊 Season {season} Overview")
season_df = matches[matches['season'] == season]
team_df = matches[matches['winner'] == team]
col1, col2 = st.columns(2)
col1.metric("Total Matches", len(season_df))
col2.metric(f"{team} Wins", len(team_df))

# Team Wins Plot
st.subheader("🏆 Most Successful Teams")
top_teams = matches['winner'].value_counts().head(10)
st.bar_chart(top_teams)

# Top Batsmen
st.subheader("🏏 Top Run Scorers")
top_batsmen = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_batsmen)

# Top Bowlers
st.subheader("🎯 Top Wicket Takers")
wickets = deliveries[deliveries['dismissal_kind'].isin(
    ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
)]
top_bowlers = wickets['bowler'].value_counts().head(10)
st.bar_chart(top_bowlers)

# Toss Decision
st.subheader("🪙 Toss Decision")
toss_decision = matches['toss_decision'].value_counts()
st.bar_chart(toss_decision)

# Player of the Match
st.subheader("🌟 Player of the Match Awards")
pom = matches['player_of_match'].value_counts().head(10)
st.bar_chart(pom)

st.markdown("Made with ❤️ using Streamlit")
