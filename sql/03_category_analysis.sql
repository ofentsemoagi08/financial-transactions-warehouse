-- Category Analysis
-- Purpose: Analyse transaction performance by category

SELECT
    c.category_name,
    COUNT(f.transaction_id) AS transaction_count,
    ROUND(SUM(f.transaction_amount), 2) AS total_spending,
    ROUND(AVG(f.transaction_amount), 2) AS average_transaction
FROM fact_transactions f
JOIN dim_category c
    ON f.category_id = c.category_id
GROUP BY
    c.category_name
ORDER BY
    total_spending DESC;
