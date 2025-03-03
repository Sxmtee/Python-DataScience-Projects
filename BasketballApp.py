import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import requests

st.title("NBA Player Stats Explorer")

st.markdown("""
    This app performs simple webscraping of NBA player stats data!
    * **Python libraries:** base64, pandas, streamlit, requests
    * **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

# Side-bar
st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox("Year", list(reversed(range(1950, 2025))))

# Web scraping of NBA player stats
@st.cache_data
def load_data(year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            st.error(f"Failed to fetch data: HTTP {response.status_code} for URL {url}")
            return None
        html = pd.read_html(response.text, header=0)
        if not html:
            st.error("No tables found in the HTML!")
            return None
        df = html[0]
        raw = df.drop(df[df.Age == "Age"].index)
        raw = raw.fillna(0)  # Still filling all with 0 for simplicity
        player_stats = raw.drop(["Rk"], axis=1, errors="ignore")
        return player_stats
    except Exception as e:
        st.error(f"Error loading data for {year}: {e}")
        return None

player_stats = load_data(selected_year)

if player_stats is not None:
    # Find team column dynamically
    team_column = next((col for col in player_stats.columns if col.lower() in ["tm", "team"]), None)
    if team_column is None:
        st.error("No team column found in the data!")
    else:
        unique_teams = player_stats[team_column].unique()
        sorted_unique_team = sorted(unique_teams, key=str)  # Convert to string for sorting
        selected_team = st.sidebar.multiselect("Team", sorted_unique_team, sorted_unique_team)

        # Sidebar - Position selection
        unique_pos = ["C", "PF", "SF", "SG", "PG"]
        selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

        # Filtering data
        df_selected_team = player_stats[(player_stats[team_column].isin(selected_team)) & 
                                        (player_stats.Pos.isin(selected_pos))]

        st.write(f"Data Dimension: {df_selected_team.shape[0]} rows and {df_selected_team.shape[1]} columns.")
        st.dataframe(df_selected_team)
else:
    st.write("No data available for the selected year.")

# Download NBA player stats data
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv">Download CSV File</a>'
    return href

st.markdown(file_download(df_selected_team), unsafe_allow_html=True)

# Heatmap
# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv', index=False)
    df = pd.read_csv('output.csv')

    # Select only numeric columns
    numeric_df = df.select_dtypes(include=['float64', 'int64'])

    # Compute correlation matrix
    corr = numeric_df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)  # Pass the figure object to st.pyplot()
