import requests
import os 
import csv
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM


# Construct the URL for the API call
symbol = 'AAPL'
api_key = 'OQLLSP66PGYDG45E'
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={api_key}&outputsize=full'


# Make the API call and retrieve the data
response = requests.get(url)
data = response.json()
time_series_daily = data['Time Series (Daily)']

# Create a CSV file and write the headers to it
with open('stock_data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    headers = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    csv_writer.writerow(headers)

    # Loop through the historic stock data and write it to the CSV file
    for date, daily_data in time_series_daily.items():
        row = [date, daily_data['1. open'], daily_data['2. high'], daily_data['3. low'], daily_data['4. close'], daily_data['6. volume']]
        csv_writer.writerow(row)

# Close the CSV file
csv_file.close()


data = pd.read_csv('stock_data.csv')


# Create a new dataframe with only the 'Close column 
df = data.filter(['Close'])
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


import pickle

# define the filename and path for your .pickle file
filename = 'model.pickle'

# open a file object in write mode
with open(filename, 'wb') as file:
    # use the pickle.dump() method to write the trained model object to the file object
    pickle.dump(model, file)

# close the file object
file.close()