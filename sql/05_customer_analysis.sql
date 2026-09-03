-- Customer Analysis
-- Purpose: Identify the top 10 customers by transaction value

SELECT
    c.customer_id,
    c.customer_name,
    c.region,
    COUNT(f.transaction_id) AS transaction_count,
    ROUND(SUM(f.transaction_amount), 2) AS total_spending,
    ROUND(AVG(f.transaction_amount), 2) AS average_transaction
FROM fact_transactions f
JOIN dim_customer c
    ON f.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.region
ORDER BY
    total_spending DESC
LIMIT 10;
