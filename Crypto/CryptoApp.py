import base64
from bs4 import BeautifulSoup
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
import requests
import seaborn as sns
import streamlit as st
import time

# Page Layout--------------------------------#
st.set_page_config(page_title='Crypto Price App', layout='wide')

# Image
image = Image.open('/Users/mac/Code/Python Projects/Crypto/logo.jpg')
st.image(image, use_container_width=True)

st.title("Crypto Price App")
st.markdown(""" 
    This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!
""")

# About
expander_bar = st.expander("About")
expander_bar.markdown("""
    * **Python libraries:** base64, pandas, streamlit
    * **Data source:** [CoinMarketCap](http://coinmarketcap.com)
    * **Credit:** App built by [Chanin Nantasenamat](http://twitter.com/thedataprof)  
""")

# Page Layout--------------------------------#
# Divide the page into 3 columns
col1 = st.sidebar
col2, col3 = st.columns((2, 1))

# Sidebar + Main panel
col1.header('Input Options')

# Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

# Web scraping of CoinMarketCap data
@st.cache_data
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {}
    coin_data = json.loads(data.contents[0])
    listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
    for i in listings:
        coins[str(i['id'])] = i['slug']

    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    for i in listings:
        coin_name.append(i['slug'])
        coin_symbol.append(i['symbol'])
        price.append(i['quote'][currency_price_unit]['price'])
        percent_change_1h.append(i['quote'][currency_price_unit]['percentChange1h'])
        percent_change_24h.append(i['quote'][currency_price_unit]['percentChange24h'])
        percent_change_7d.append(i['quote'][currency_price_unit]['percentChange7d'])
        market_cap.append(i['quote'][currency_price_unit]['marketCap'])
        volume_24h.append(i['quote'][currency_price_unit]['volume24h'])
    
    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df

df = load_data()

# Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['coin_symbol'] )
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

# Filtering data
df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin)) ]