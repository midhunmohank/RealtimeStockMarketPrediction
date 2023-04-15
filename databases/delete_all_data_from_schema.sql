CREATE PROCEDURE [dbo].[DeleteAllPredictionAndGraphData]
AS
BEGIN
    -- Disable foreign key constraints
    ALTER TABLE [dbo].[PriceEdge] NOCHECK CONSTRAINT ALL;

    -- Delete data from PredictionTable
    DELETE FROM [dbo].[PredictionTable];

    -- Delete data from PriceEdge table
    DELETE FROM [dbo].[PriceEdge];

    -- Enable foreign key constraints
    ALTER TABLE [dbo].[PriceEdge] CHECK CONSTRAINT ALL;
END;
