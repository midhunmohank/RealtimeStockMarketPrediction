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