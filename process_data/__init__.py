import json
import pandas as pd
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_body().decode('utf-8')
        data = json.loads(req_body)

        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Date', '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '6. volume': 'Volume'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'])
        df['Date'] = df['Date'].dt.date
        df['Open'] = df['Open'].astype(float)
        df['High'] = df['High'].astype(float)
        df['Low'] = df['Low'].astype(float)
        df['Close'] = df['Close'].astype(float)
        df['Volume'] = df['Volume'].astype(int)
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df = df.sort_values(by='Date', ascending=False)
        df = df.reset_index(drop=True)

        # Return the dataframe as CSV
        csv_string = df.to_csv(index=False)

    except ValueError:
        return func.HttpResponse(
            "Invalid JSON format in request body",
            status_code=400
        )

    return func.HttpResponse(
        csv_string,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=stock_data.csv'}
    )


# import json
# import pandas as pd
# import azure.functions as func
# from datetime import datetime
# from sqlalchemy import create_engine

# def main(req: func.HttpRequest) -> func.HttpResponse:
#     try:
#         req_body = req.get_body().decode('utf-8')
#         data = json.loads(req_body)

#         # Extract data from "Time Series (Daily)" object
#         df = pd.json_normalize(data['Time Series (Daily)'], meta=['date'])

#         # Rename columns
#         df.rename(columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '6. volume': 'Volume', 'date': 'Date'}, inplace=True)

#         # Check if columns exist before dropping them
#         columns_to_drop = ['5. adjusted close', '7. dividend amount', '8. split coefficient']
#         for col in columns_to_drop:
#             if col in df.columns:
#                 df.drop(columns=[col], inplace=True)

#         # Reorder columns
#         df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

#         # Connect to SQL Server database using SQL Alchemy
#         server = 'stockdata.database.windows.net'
#         database = 'stockdata'
#         username = 'stocks'
#         password = '@Damg2023'
#         driver = '{ODBC Driver 17 for SQL Server}'
#         conn_string = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
#         engine = create_engine(conn_string)

#         # Insert data into relational database using SQL Alchemy
#         with engine.connect() as conn:
#             # Insert date into DateNode table
#             for date in df['Date'].unique():
#                 conn.execute("INSERT INTO DateNode (date_id) VALUES (?)", datetime.strptime(date, '%Y-%m-%d').date())

#             # Insert price data into PriceEdge table
#             for _, row in df.iterrows():
#                 # Get date_id from DateNode table
#                 date_id = conn.execute("SELECT date_id FROM DateNode WHERE date_id = ?", datetime.strptime(row['Date'], '%Y-%m-%d').date()).fetchone()[0]

#                 # Insert data into PriceEdge table
#                 conn.execute("""
#                     INSERT INTO PriceEdge (date_id, open_price, high_price, low_price, close_price, volume)
#                     VALUES (?, ?, ?, ?, ?, ?)
#                 """, date_id, row['Open'], row['High'], row['Low'], row['Close'], row['Volume'])

#     except ValueError:
#         return func.HttpResponse(
#             "Invalid JSON format in request body",
#             status_code=400
#         )

#     return func.HttpResponse("Data successfully loaded into Azure SQL Database.")
