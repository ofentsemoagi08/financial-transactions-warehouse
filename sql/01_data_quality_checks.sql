-- Data Quality Checks
-- Purpose: Validate the integrity of the warehouse fact table

-- 1. Check total fact rows
SELECT
    COUNT(*) AS total_fact_rows
FROM fact_transactions;


-- 2. Check for missing foreign keys
SELECT
    COUNT(*) AS rows_with_missing_keys
FROM fact_transactions
WHERE customer_id IS NULL
   OR category_id IS NULL
   OR date_id IS NULL;


-- 3. Check for duplicate transaction IDs
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT transaction_id) AS unique_transactions
FROM fact_transactions;


-- 4. Check transaction amounts
SELECT
    COUNT(*) AS total_transactions,
    COUNT(transaction_amount) AS transactions_with_amount,
    COUNT(*) FILTER (
        WHERE transaction_amount <= 0
    ) AS invalid_amounts,
    ROUND(MIN(transaction_amount), 2) AS minimum_amount,
    ROUND(MAX(transaction_amount), 2) AS maximum_amount
FROM fact_transactions;
