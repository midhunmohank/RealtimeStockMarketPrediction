
import sqlalchemy as sa
from sqlalchemy import create_engine
from urllib.parse import quote_plus

server = 'stockpricedb.database.windows.net'
database = 'stockdata'
username = 'stocks'
password = '@Damg2023'
port = '1433'
driver = '{ODBC Driver 18 for SQL Server}'  # Update this to match your installed ODBC driver

# Create the connection string using pyodbc
conn_str = f"DRIVER={driver};SERVER={server},{port};DATABASE={database};UID={username};PWD={password}"

# Create the engine using sqlalchemy
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quote_plus(conn_str)}")

# Create a connection
conn = engine.connect()

# Create a table
conn.execute("CREATE TABLE test (id int, data varchar(255))")