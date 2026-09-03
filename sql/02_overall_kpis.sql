-- Overall Warehouse KPIs
-- Purpose: High-level transaction performance metrics

SELECT
    COUNT(*) AS total_transactions,
    ROUND(SUM(transaction_amount), 2) AS total_transaction_value,
    ROUND(AVG(transaction_amount), 2) AS average_transaction_value,
    ROUND(MIN(transaction_amount), 2) AS minimum_transaction_value,
    ROUND(MAX(transaction_amount), 2) AS maximum_transaction_value
FROM fact_transactions;
