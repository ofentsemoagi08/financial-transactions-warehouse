-- Monthly Transaction Analysis
-- Purpose: Analyse transaction performance by month

SELECT
    d.year,
    d.month,
    COUNT(f.transaction_id) AS transaction_count,
    ROUND(SUM(f.transaction_amount), 2) AS total_spending,
    ROUND(AVG(f.transaction_amount), 2) AS average_transaction
FROM fact_transactions f
JOIN dim_date d
    ON f.date_id = d.date_id
GROUP BY
    d.year,
    d.month
ORDER BY
    total_spending DESC;
