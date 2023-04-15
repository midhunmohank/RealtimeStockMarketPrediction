import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from utils import fetch_insert_predict

def app():
    # Create a selectbox for the user to choose a stock
    symbol = st.sidebar.selectbox('Select a stock', ('AAPL', 'MSFT', 'GOOGL'))

    # Create a button to fetch the stock data
    if st.sidebar.button('Fetch data and Predict'):
        history, predictions = fetch_insert_predict(symbol)

        #Spinner to show that the data is being fetched
        with st.spinner('Fetching data...'):
            st.success('Data fetched and Predictions Visualized Successfully!')

        # Create a Bokeh figure for the stock price
        source = ColumnDataSource(history)
        fig = figure(x_axis_type='datetime', title='Historical Stock Price')
        fig.line('Date', 'Close', source=source, line_width=2, color='navy')

        # Add the predictions to the figure
        if not predictions.empty:
            source = ColumnDataSource(predictions)
            fig.line('Date', 'Price', source=source, line_width=2, color='red', legend_label='Predictions')

        # Customize the plot
        fig.xaxis.axis_label = 'Date'
        fig.yaxis.axis_label = 'Stock Price'

        # Display the chart in the Streamlit app
        st.bokeh_chart(fig, use_container_width=True)


if __name__ == '__main__':
    app()
