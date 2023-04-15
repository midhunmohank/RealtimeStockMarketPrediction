
CREATE PROCEDURE [dbo].[InsertCSVData]
    @csv NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    -- Create temp table to hold CSV data
    IF OBJECT_ID('tempdb..#temp') IS NOT NULL
        DROP TABLE #temp;

    CREATE TABLE #temp (
        [symbol] NVARCHAR(10),
        [date] DATE,
        [open_price] FLOAT,
        [high_price] FLOAT,
        [low_price] FLOAT,
        [close_price] FLOAT,
        [volume] BIGINT
    );

    -- Construct dynamic SQL to execute BULK INSERT statement
    DECLARE @sql NVARCHAR(MAX);
    SET @sql = N'INSERT INTO #temp ([symbol], [date], [open_price], [high_price], [low_price], [close_price], [volume])
                SELECT *
                FROM OPENROWSET(
                    BULK ''' + REPLACE(@csv, '''', '''''') + N''',
                    FORMAT=''CSV'',
                    FIRSTROW = 2,
                    MAXERRORS = 0,
                    FIELDTERMINATOR = '','',
                    ROWTERMINATOR = ''\n''
                ) AS data';
    EXEC sp_executesql @sql;

    -- Insert data into DateNode table
    INSERT INTO DateNode (date_id)
    SELECT DISTINCT [date]
    FROM #temp
    WHERE [date] NOT IN (SELECT date_id FROM DateNode);

    -- Insert data into StockNode table
    INSERT INTO StockNode (symbol)
    SELECT DISTINCT [symbol]
    FROM #temp
    WHERE [symbol] NOT IN (SELECT symbol FROM StockNode);

    -- Insert data into PriceEdge table
    INSERT INTO PriceEdge (date_id, symbol_id, open_price, high_price, low_price, close_price, volume)
    SELECT d.date_id, s.symbol_id, t.open_price, t.high_price, t.low_price, t.close_price, t.volume
    FROM #temp t
    JOIN DateNode d ON t.date = d.date_id
    JOIN StockNode s ON t.symbol = s.symbol;

    -- Insert data into PriceEdge_Relationship table
    INSERT INTO PriceEdge_Relationship (from_id, to_id)
    SELECT DISTINCT d.date_id, s.symbol_id
    FROM #temp t
    JOIN DateNode d ON t.date = d.date_id
    JOIN StockNode s ON t.symbol = s.symbol
    WHERE NOT EXISTS (
        SELECT *
        FROM PriceEdge_Relationship pr
        WHERE pr.from_id = d.date_id AND pr.to_id = s.symbol_id
    );

    -- Drop temp table
    DROP TABLE #temp;
END

