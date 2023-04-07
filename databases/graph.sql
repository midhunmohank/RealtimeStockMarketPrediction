-- Create the Date node
CREATE TABLE [dbo].[DateNode] (
 [date_id] DATE NOT NULL PRIMARY KEY,
) AS NODE;
GO


-- Create the Stock node
CREATE TABLE [dbo].[StockNode] (
 [symbol] NVARCHAR(10) NOT NULL PRIMARY KEY,
) AS NODE;
GO


-- Create the PriceEdge table
CREATE TABLE [dbo].[PriceEdge] (
 [date_id] DATE NOT NULL,
 [symbol] NVARCHAR(10) NOT NULL,
 [open_price] FLOAT NOT NULL,
 [high_price] FLOAT NOT NULL,
 [low_price] FLOAT NOT NULL,
 [close_price] FLOAT NOT NULL,
 [volume] BIGINT NOT NULL,
 PRIMARY KEY ([date_id], [symbol]),
 FOREIGN KEY ([date_id]) REFERENCES [dbo].[DateNode] ([date_id]),
 FOREIGN KEY ([symbol]) REFERENCES [dbo].[StockNode] ([symbol])
) AS EDGE;
GO


-- Create the relationship between the Date and Stock nodes via the PriceEdge table
CREATE TABLE [dbo].[PriceEdge_Relationship] (
 [from_id] DATE NOT NULL,
 [to_id] NVARCHAR(10) NOT NULL,
 PRIMARY KEY ([from_id], [to_id]),
 FOREIGN KEY ([from_id]) REFERENCES [dbo].[DateNode] ([date_id]),
 FOREIGN KEY ([to_id]) REFERENCES [dbo].[StockNode] ([symbol])
) AS EDGE;
GO
