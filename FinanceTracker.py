import streamlit as st
import pandas as pd
import yfinance as yf

st.write(''' 
    # Simple Stock Price App

    Shown are the stock **closing price** and ***volume*** of Google!
''')

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

# define the ticker symbol
tickerSymbol = "GOOGL"

# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# get the historical prices for this ticker
tickerDf = tickerData.history(period="1d", start="2010-5-21", end="2020-5-21")

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)