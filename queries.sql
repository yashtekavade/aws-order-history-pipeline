-- 1. Top 10 High Value Orders
SELECT OrderID, TotalAmountUSD
FROM tbsm_red_transformed
WHERE OrderTag = 'High'
ORDER BY TotalAmountUSD DESC
LIMIT 10;

-- 2. Average Order Value by Country
SELECT Country, AVG(TotalAmountUSD) as avg_value
FROM tbsm_red_transformed
GROUP BY Country;

-- 3. Daily Order Trends
SELECT InvoiceDateOnly, COUNT(*) as orders, SUM(TotalAmountUSD) as revenue
FROM tbsm_red_transformed
GROUP BY InvoiceDateOnly
ORDER BY InvoiceDateOnly;

-- 4. Region-wise Distribution
SELECT Region, COUNT(*) as order_count
FROM tbsm_red_transformed
GROUP BY Region;

-- 5. Peak Order Time
SELECT InvoiceHour, COUNT(*) as orders
FROM tbsm_red_transformed
GROUP BY InvoiceHour
ORDER BY InvoiceHour;

-- 6. Query Specific Partition (UK Orders)
SELECT * FROM tbsm_red_transformed
WHERE Country = 'United Kingdom';
