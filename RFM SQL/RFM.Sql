WITH lod as ( 
SELECT customer_id, payment_date as last_payment_date
FROM (
SELECT customer_id, 
payment_date, 
DENSE_RANK() over(PARTITION by customer_id ORDER BY payment_date DESC) as rnk_
FROM payment) as lpd
WHERE rnk_ = 1
ORDER BY random() )

, mon as (
SELECT customer_id,
COUNT(payment_id) count_trans,
SUM(amount) total_amount
FROM payment
GROUP by 1 )


, rfm_value as (
SELECT mon.customer_id,
DATE(LOD.last_payment_date) last_payment_date,
DATE_PART('DAY', '2007-05-16' - LOD.last_payment_date) recency,
mon.count_trans as freq,
mon.total_amount as amount

FROM mon
LEFT JOIN LOD 
ON LOD.customer_id = mon.customer_id)


, rfm as (
SELECT * 
, NTILE(4) OVER (ORDER BY recency DESC) AS R 
, NTILE(4) OVER (ORDER BY freq DESC ) AS F 
, NTILE(4) OVER (ORDER BY amount DESC ) AS M 
FROM rfm_value
ORDER BY RANDOM()
)

, rfm_class as (
SELECT * 
, CONCAT(R, F, M) as rfm_class
FROM rfm
)

, rfm_cat as (
SELECT *
, CASE 
    WHEN rfm_class SIMILAR TO '1[1-2][1-2]' THEN 'Best Customers'
    WHEN rfm_class SIMILAR TO '14[1-2]' THEN 'High-spending New Customers' 
    WHEN rfm_class SIMILAR TO '11[3-4]' THEN 'Lowest-Spending Active Loyal Customers' 
    WHEN rfm_class SIMILAR TO '4[1-2][1-2]' THEN 'Churned Best Customers' 
ELSE NULL 
END AS rfm_category 
FROM rfm_class)

-- SELECT rfm_category,
-- COUNT(customer_id) as cnt
-- from rfm_cat 
-- GROUP by 1

SELECT rc.customer_id
, cs.first_name
, cs.email
, rc.rfm_class
, rc.rfm_category
FROM rfm_cat rc
LEFT join customer cs
on cs.customer_id = rc.customer_id;