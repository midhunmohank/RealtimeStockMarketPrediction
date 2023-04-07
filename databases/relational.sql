CREATE TABLE stock_data (
   id INT IDENTITY(1,1) PRIMARY KEY,
   open_price FLOAT NOT NULL,
   close_price FLOAT NOT NULL,
   date DATE NOT NULL,
   high FLOAT NOT NULL,
   low FLOAT NOT NULL,
   adjusted_close FLOAT NOT NULL,
   volume INT NOT NULL
);


ALTER TABLE stock_data
ADD symbol VARCHAR(10);




CREATE TABLE prediction (
 symbol VARCHAR(10),
 predicted_open DECIMAL(10, 2),
 predicted_close DECIMAL(10, 2)
);


CREATE TABLE stocks (
 stockid INT PRIMARY KEY,
 company_name VARCHAR(50),
 symbol VARCHAR(10)
);


CREATE TABLE companies (
 company_name VARCHAR(50) PRIMARY KEY,
 sector_name VARCHAR(50)
);
