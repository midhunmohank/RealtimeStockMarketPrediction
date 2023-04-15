CREATE PROCEDURE [dbo].[InsertPrediction]
    @symbol NVARCHAR(10),
    @date DATE,
    @prediction_price FLOAT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @predictionData NVARCHAR(MAX);
    SET @predictionData = N'{"symbol":"' + REPLACE(@symbol, '"', '\"') + N'", "date":"' + CONVERT(NVARCHAR(10), @date, 126) + N'", "prediction_price":' + CONVERT(NVARCHAR(30), @prediction_price) + N'}';

    INSERT INTO PredictionTable ([symbol], [date], [prediction_data])
    VALUES (@symbol, @date, @predictionData);
END
