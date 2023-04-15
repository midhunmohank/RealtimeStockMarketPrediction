-- Create the Company table
CREATE TABLE [dbo].[Company] (
    [company_id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [company_name] NVARCHAR(100) NOT NULL,
    [symbol] NVARCHAR(10) NOT NULL UNIQUE
);

-- Create the StockNode table
CREATE TABLE [dbo].[StockNode] (
    [symbol_id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [symbol] NVARCHAR(10) NOT NULL UNIQUE
);

-- Create the DateNode table
CREATE TABLE [dbo].[DateNode] (
    [date_id] DATE NOT NULL PRIMARY KEY
) AS NODE;

-- Create the PriceEdge table
CREATE TABLE [dbo].[PriceEdge] (
    [edge_id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [date_id] DATE NOT NULL,
    [symbol_id] INT NOT NULL,
    [open_price] FLOAT NOT NULL,
    [high_price] FLOAT NOT NULL,
    [low_price] FLOAT NOT NULL,
    [close_price] FLOAT NOT NULL,
    [volume] BIGINT NOT NULL,
    FOREIGN KEY ([date_id]) REFERENCES [dbo].[DateNode] ([date_id]),
    FOREIGN KEY ([symbol_id]) REFERENCES [dbo].[StockNode] ([symbol_id])
);

-- Create the PredictionTable
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
