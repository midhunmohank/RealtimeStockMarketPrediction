import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px


def app():
    # Create a selectbox for the user to choose a stock
    symbol = st.sidebar.selectbox('Select a stock', ('AAPL', 'MSFT', 'GOOGL'))

    # Use yfinance to retrieve stock data
    stock_data = yf.Ticker(symbol).history(period="max")

    # Create a line chart using Plotly Express
    fig = px.line(stock_data, x=stock_data.index, y='Close')

    # Display the chart using Streamlit
    st.plotly_chart(fig)


if __name__ == '__main__':
    app()
# import requests
# import json

# url = "https://prod-10.eastus.logic.azure.com/workflows/f737c591a08d423f95455787032d3d60/triggers/manual/paths/invoke/recievesymbol?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=po8AR58-CTucTwOKp3tR379yNJASY2jYlGj56HYrp_w"

# data = {"symbol": "AAPL"}
# headers = {"Content-Type": "application/json"}

# response = requests.post(url, data=json.dumps(data), headers=headers)

# print(response.status_code)
# print(response.text)
