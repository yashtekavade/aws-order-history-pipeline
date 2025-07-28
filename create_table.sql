CREATE EXTERNAL TABLE IF NOT EXISTS tbsm_red_transformed (
  CustomerID INT,
  OrderID STRING,
  InvoiceNo STRING,
  StockCode STRING,
  Description STRING,
  Quantity FLOAT,
  UnitPrice FLOAT,
  TotalAmount FLOAT,
  TotalAmountUSD FLOAT,
  OrderTag STRING,
  InvoiceDate STRING,
  InvoiceDateOnly DATE,
  InvoiceHour INT,
  Country STRING,
  Region STRING
)
PARTITIONED BY (
  Country STRING,
  InvoiceDateOnly DATE
)
STORED AS PARQUET
LOCATION 's3://tbsm-red/target/';
