-- ===========================
-- Dimension: Customer
--  ==========================
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    region VARCHAR(50),
    age_group VARCHAR(20)
);

-- ===========================
-- Dimension: Category
-- ===========================
CREATE TABLE dim_category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE
);

-- ===========================
-- Dimension: Date
-- ===========================
CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    full_date DATE UNIQUE,
    day INT,
    month INT,
    quarter INT,
    year INT
);

-- ===========================
-- Fact: Transactions
-- ===========================
CREATE TABLE fact_transactions (
    transaction_id INT PRIMARY KEY,

    customer_id INT
        REFERENCES dim_customer(customer_id),

    category_id INT
        REFERENCES dim_category(category_id),

    date_id INT
        REFERENCES dim_date(date_id),

    transaction_amount DECIMAL(12,2)
);