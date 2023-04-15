import os
import sqlalchemy as sa
from sqlalchemy import create_engine,text
from urllib.parse import quote_plus
import requests
import json
import pickle
import pandas as pd
from io import StringIO
import pickle
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
import datetime
from sklearn.metrics import mean_squared_error

server = 'stockpricedb.database.windows.net'
database = 'stockdata'
username = 'stocks'
password = '@Damg2023'
port = '1433'
driver = '{ODBC Driver 18 for SQL Server}'  

# Create the connection string using pyodbc
conn_str = f"DRIVER={driver};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}"

# Create the engine using sqlalchemy
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}")

# function to get data from API

def fetch_insert_predict(symbol):
    url = "https://prod-24.eastus.logic.azure.com/workflows/b1b12041d2314ea89a8fb9efac19694d/triggers/manual/paths/invoke/recievesymbol?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=3sj5UtrIbVLPq495s2h3mt8Fq8PRt-d0BFwdsaS81l4"

    payload = json.dumps({
      "symbol": symbol
    })
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    #sample response
    """{
    "symbol": "MSFT",
    "csv": "Date,Open,High,Low,Close,Volume\n2023-04-14,287.0,288.48,283.69,286.14,20987917\n2023-04-13,283.59,289.9,283.17,289.84,24222678\n2023-04-12,284.79,287.01,281.96,283.49,27403432\n2023-04-11,285.75,285.98,281.64,282.83,27276589\n2023-04-10,289.208,289.6,284.71,289.39,23102994\n2023-04-06,283.21,292.08,282.03,291.6,29770334\n2023-04-05,285.85,287.15,282.92,284.34,22064770\n2023-04-04,287.23,290.4499,285.67,287.18,25824299\n2023-04-03,286.52,288.27,283.95,287.23,24883342\n2023-03-31,283.73,289.27,283.0,288.3,32765976\n2023-03-30,284.23,284.46,281.48,284.05,25053410\n2023-03-29,278.96,281.1398,278.41,280.51,25087032\n2023-03-28,275.79,276.14,272.0451,275.23,21878647\n2023-03-27,280.5,281.4589,275.52,276.38,26840212\n}"""

    #convert response to json
    response = json.loads(response.text)
    #Extract symbol 
    symbol = response['symbol']
    #Extract csv
    csv = response['csv']
    #Convert csv to dataframe
    Price_edge = pd.read_csv(StringIO(csv))
    #Insert symbol into stock node
    with engine.connect() as conn:
        query = text(f"INSERT INTO StockNode values ('{symbol}');commit;")
        conn.execute(query)
    
    #Retreive symbol_id from stock node
    with engine.connect() as conn:
        query= text(f"SELECT symbol_id FROM StockNode WHERE symbol = '{symbol}';")
        result = conn.execute(query)
        symbol_id = result.fetchall()[0][0]
    
    # Process price edge based on price edge table schema
    Price_edge['Date'] = pd.to_datetime(Price_edge['Date'])
    Price_edge['Date'] = Price_edge['Date'].dt.strftime('%Y-%m-%d')

    # #Insert Date from price_edge into DateNode
    with engine.connect() as conn:
        for index, row in Price_edge.iterrows():
            query = text(f"INSERT INTO DateNode values ('{row['Date']}');commit;")
            conn.execute(query)


    #Insert Historical price data into price edge
    for index, row in Price_edge.iterrows():
        with engine.connect() as conn:
            query = text(f"INSERT INTO PriceEdge values ('{row['Date']}',{symbol_id},{row['Open']},{row['High']},{row['Low']},{row['Close']},{row['Volume']});commit;")
            conn.execute(query)
    
    #Retreive price edge
    with engine.connect() as conn:
        query = text(f"SELECT * FROM PriceEdge WHERE symbol_id = {symbol_id};")
        result = conn.execute(query)
        historic_price_from_graph = result.fetchall()
  
    #Convert Historic price edge to dataframe
    historic_price_from_graph = pd.DataFrame(historic_price_from_graph, columns=['row','Date','symbol_id','Open','High','Low','Close','Volume'])

    #Drop row column
    historic_price_from_graph = historic_price_from_graph.drop(columns=['row'])

    #Convert Date to datetime
    historic_price_from_graph['Date'] = pd.to_datetime(historic_price_from_graph['Date'])

    #Convert Date to string
    historic_price_from_graph['Date'] = historic_price_from_graph['Date'].dt.strftime('%Y-%m-%d')

    
    #Predicting the stock price

  # Create a new dataframe with only the 'Close column 
    df = historic_price_from_graph.filter(['Close'])
    # Convert the dataframe to a numpy array
    dataset = df.values
    # Get the number of rows to train the model on
    training_data_len = int(np.ceil( len(dataset) * .95 ))

    training_data_len

    # Scale the data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    scaled_data

    # Create the training data set 
    # Create the scaled training data set
    train_data = scaled_data[0:int(training_data_len), :]
    # Split the data into x_train and y_train data sets
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
        if i<= 61:
            print(x_train)
            print(y_train)
            print()
        
    # Convert the x_train and y_train to numpy arrays 
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    # x_train.shape
    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape= (x_train.shape[1], 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Create the testing data set
    # Create a new array containing scaled values from index 1543 to 2002 
    test_data = scaled_data[training_data_len - 60: , :]
    # Create the data sets x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])
        
    # Convert the data to a numpy array
    x_test = np.array(x_test)

    # Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

    # Get the models predicted price values 
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)

    Predictions = pd.DataFrame(predictions, columns=['Predictions'])
    # Return the predicted target values


    # Calculate the mean squared error (MSE)
    mse = mean_squared_error(y_test, predictions)

    # Calculate the model accuracy score
    accuracy_score = 1 - mse / np.var(y_test)
    #Predictions schema
    """-- Create the PredictionTable
CREATE TABLE [dbo].[PredictionTable] (
    [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [symbol] NVARCHAR(10) NOT NULL,
    [date] DATE NOT NULL,
    [prediction_data] NVARCHAR(MAX) NOT NULL,
    [CreatedAt] DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    INDEX [ix_symbol_date] NONCLUSTERED (symbol, date)
);

-- Add JSON column to store prediction data
ALTER TABLE [dbo].[PredictionTable]
ADD [prediction_data_json] AS JSON_QUERY([prediction_data]);
"""
    #Create dates dataframe from current day to 5 days from now
    current_date = datetime.datetime.now()
    dates = pd.date_range(current_date, periods=5, freq='D')
    dates = dates.strftime('%Y-%m-%d')
    dates = pd.DataFrame(dates, columns=['Date'])

    #Create prediction dataframe
    predictions = pd.concat([dates, Predictions], axis=1)
    predictions = predictions.dropna()

    #Convert Date to datetime to 
    predictions['Date'] = pd.to_datetime(predictions['Date'])

    #Convert Date to string
    predictions['Date'] = predictions['Date'].dt.strftime('%Y-%m-%d')

    #Insert predictions into PredictionTable

    for index, row in predictions.iterrows():
        with engine.connect() as conn:
            query = text(f"INSERT INTO PredictionTable (symbol, date, prediction_data) VALUES ('{symbol}', '{row['Date']}', '{row['Predictions']}');")
            conn.execute(query)

    #Return historic and predictions
    return predictions, historic_price_from_graph






