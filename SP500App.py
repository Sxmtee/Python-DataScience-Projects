import base64
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import yfinance as yf

st.title("S&P 500 App")

st.markdown(""" 
    This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
    * **Python libraries:** base64, matplotlib, pandas, streamlit, yfinance
    * **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

# Sidebar
st.sidebar.header("User Input Features")

# Web scraping of S&P 500 data
@st.cache_data
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby("GICS Sector")

# Sidebar - Sector selection
sorted_sector_unique = sorted(df["GICS Sector"].unique())
selected_sector = st.sidebar.multiselect("Sector", sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[(df["GICS Sector"].isin(selected_sector))]

st.header("Display Companies in Selected Sector")
st.write(f"Data Dimension: {df_selected_sector.shape[0]} rows and {df_selected_sector.shape[1]} columns.")
st.dataframe(df_selected_sector)

# Download S&P 500 data
def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(file_download(df_selected_sector), unsafe_allow_html=True)

# Descriptive statistics
st.write(df_selected_sector.describe())

# Plots
st.header("Stock Closing Price")
df_selected_sector.set_index("Symbol", inplace=True)

data = yf.download(
    tickers=list(df_selected_sector[:10].index),
    start="2020-01-01",
    end="2020-12-31",
    progress=False
)

# Plot closing price of query symbol
def price_plot(symbol):
    if symbol not in data.columns.get_level_values(1):
        st.write(f"No data available for {symbol}")
        return None
    
    df = pd.DataFrame(data[('Close', symbol)])
    df.columns = ['Close']
    df["Date"] = df.index
    
    plt.figure(figsize=(10, 4))
    plt.fill_between(df.Date, df.Close, color="skyblue", alpha=0.3)
    plt.plot(df.Date, df.Close, color="skyblue", alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight="bold")
    plt.xlabel("Date", fontweight="bold")
    plt.ylabel("Closing Price", fontweight="bold")
    return st.pyplot(plt)

num_company = st.sidebar.slider("Number of Companies", 1, 5)

if st.button("Show Plots"):
    st.header("Stock Closing Price")
    for i in list(df_selected_sector.index[:num_company]):
        price_plot(i)