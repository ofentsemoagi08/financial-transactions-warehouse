import pandas as pd
from datetime import datetime

customers_df = pd.read_csv("data/raw/customers_raw.csv")
categories_df = pd.read_csv("data/raw/categories_raw.csv")
transactions_df = pd.read_csv("data/raw/transactions_raw.csv")

##sanity check

print("Customers loaded:", customers_df.shape)
print("Categories loaded:", categories_df.shape)
print("Transactions loaded:", transactions_df.shape)

#detect missing customer names

print("\n--- Missing Customer Names ---")
missing_names = customers_df["customer_name"].isnull().sum()
print("Missing customer names:", missing_names)

#detect missing age groups

print("\n--- Missing Age Groups ---")
missing_age_groups = customers_df["age_group"].isnull().sum()
print("Missing age groups:", missing_age_groups)

#detect duplicate names

print("\n--- Duplicate Customers ---")
duplicate_customers = customers_df.duplicated().sum()
print("Duplicate customer records:", duplicate_customers)

#detect invalid regions

valid_regions = [   
    "Western Cape",
    "Gauteng",
    "KwaZulu-Natal",
    "Eastern Cape",
    "Free State"
]

print("\n--- Invalid Regions ---")
invalid_regions = customers_df[~customers_df["region"].isin(valid_regions)]
print("Invalid region records:", len(invalid_regions))

#invalid customer references in transactions

print("\n--- Invalid Customer References ---")
valid_customer_ids = set(customers_df["customer_id"])
invalid_customer_transactions = transactions_df[~transactions_df["customer_id"].isin(valid_customer_ids)]
print("Transactions with invalid customer IDs:",len(invalid_customer_transactions))

#detect negative transaction amounts

print("\n--- Negative Transaction Amounts ---")
negative_transactions = transactions_df[transactions_df["transaction_amount"] < 0]
print("Negative transactions:",len(negative_transactions))

#detect zero transaction amounts

print("\n--- Zero Transaction Amounts ---")
zero_transactions = transactions_df[transactions_df["transaction_amount"] == 0]
print("Zero value transactions:",len(zero_transactions))

#detect missing dates

print("\n--- Missing Transaction Dates ---")
missing_dates = transactions_df[transactions_df["transaction_date"].isnull()]
print("Missing transaction dates:",len(missing_dates))

#detect future transaction dates

print("\n--- Future-Dated Transactions ---")
transactions_df["transaction_date"] = pd.to_datetime(transactions_df["transaction_date"],errors="coerce")
today = pd.Timestamp.today()
future_transactions = transactions_df[transactions_df["transaction_date"] > today]
print("Future-dated transactions:",len(future_transactions))

#detect invalid category references in transactions

valid_categories = [
    "Groceries",
    "Transport",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Shopping"
]

print("\n--- Invalid Categories ---")
invalid_categories = transactions_df[~transactions_df["category_name"].isin(valid_categories)]
print("Invalid category transactions:",len(invalid_categories))


#quality report (create new spreedsheet)
quality_report = pd.DataFrame({
    "check_name": [
        "Missing Customer Names",
        "Missing Age Groups",
        "Duplicate Customers",
        "Invalid Regions",
        "Invalid Customer References",
        "Negative Transactions",
        "Zero Value Transactions",
        "Missing Transaction Dates",
        "Future-Dated Transactions",
        "Invalid Categories"
    ],

    "issue_count": [
        missing_names,
        missing_age_groups,
        duplicate_customers,
        len(invalid_regions),
        len(invalid_customer_transactions),
        len(negative_transactions),
        len(zero_transactions),
        len(missing_dates),
        len(future_transactions),
        len(invalid_categories)
    ]
})

quality_report.to_csv("data/reports/data_quality_report.csv",index=False)
print("\nData quality report created!")