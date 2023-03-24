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
