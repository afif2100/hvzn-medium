WITH lod as ( 
SELECT CustomerID 
, OrderDate as LastOrderDate 
FROM ( SELECT OrderID 
, CustomerID 
, OrderDate 
, DENSE_RANK() OVER (PARTITION BY CustomerID 
ORDER BY OrderDate 
DESC) AS rnk_ 
FROM orders) as date_ 
WHERE rnk_ = 1 
) 
, recency as ( 
SELECT CustomerID 
, LastOrderDate 
, DATEDIFF("1997-08-20", LastOrderDate) AS recency -- get date today in 1997 FROM lod 
ORDER BY 3 ) 
-- 
, cust_order as ( 
SELECT oo.OrderID 
, oo.OrderDate 
, oo.CustomerID 
, od.ProductID
, od.Quantity 
FROM orders AS oo 
LEFT JOIN order_details as od 
ON oo.OrderID = od.OrderID 
ORDER BY oo.CustomerID desc 
) 
, cust_spending as ( 
SELECT co.CustomerID 
, co.OrderId 
, co.OrderDate 
, pr.ProductID 
, pr.ProductName 
, (co.Quantity * pr.Price) as TSOP 
FROM cust_order AS co 
LEFT JOIN products as pr 
ON co.ProductID = pr.ProductID 
ORDER BY TSOP desc) 
, freq_mon as ( 
SELECT 
CustomerID 
, COUNT(OrderId) as freq 
, ROUND(SUM(TSOP)) as mon 
FROM cust_spending 
GROUP BY 1 ) 
-- 
, rfm as ( 
SELECT * 
, NTILE(4) OVER (ORDER BY recency DESC) AS R , NTILE(4) OVER (ORDER BY freq DESC ) AS F , NTILE(4) OVER (ORDER BY mon DESC ) AS M FROM ( 
SELECT _fm.CustomerID 
, _fm.freq 
, _fm.mon 
, _rec.LastOrderDate 
, _rec.recency 
FROM freq_mon AS _fm 
LEFT JOIN recency AS _rec 
ON _rec.CustomerID = _fm.CustomerID 
) as _rfm 
) 
-- 
, rfm_cls as ( 
SELECT CustomerID 
, recency 
, freq 
, mon 
, LastOrderDate 
, CONCAT(R, F, M) as rfm_class 
FROM rfm) 
SELECT cs.CustomerID 
, cs.CustomerName 
, rc.recency AS Recency 
, rc.freq AS Frequency 
, rc.mon AS Monetary 
, rc.LastOrderDate 
, rc.rfm_class as RFM_CLASS 
, CASE 
WHEN rfm_class regexp '1[1-2][1-2]' THEN 'Best Customers'
WHEN rfm_class regexp '14[1-2]' THEN 'High-spending New Customers' WHEN rfm_class regexp '11[3-4]' THEN 'Lowest-Spending Active Loyal Customers' WHEN rfm_class regexp '4[1-2][1-2]' THEN 'Churned Best Customers' 
ELSE NULL 
END AS rfm_category 
FROM rfm_cls AS rc 
LEFT JOIN customers as cs 
ON cs.CustomerID = rc.CustomerID 
Order by rfm_category DESC
