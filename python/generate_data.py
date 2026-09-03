import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

random.seed(42)

regions = [
    "Western Cape",
    "Gauteng",
    "KwaZulu-Natal",
    "Eastern Cape",
    "Free State"
]

age_groups = [
    "18-25",
    "26-35",
    "36-50",
    "51+"
]

customers = []

for customer_id in range(1, 1001):
    customers.append({
        "customer_id": customer_id,
        "customer_name": fake.name(),
        "region": random.choice(regions),
        "age_group": random.choice(age_groups)
    })

customers_df = pd.DataFrame(customers)

# Introduce missing customer names
missing_names = random.sample(range(len(customers_df)), 20)
customers_df.loc[missing_names, "customer_name"] = None

# Introduce invalid regions
invalid_regions = random.sample(range(len(customers_df)), 10)
customers_df.loc[invalid_regions, "region"] = "Mars Province"

# Introduce invalid age groups
missing_age_groups = random.sample(range(len(customers_df)), 15)
customers_df.loc[missing_age_groups, "age_group"] = None

# Create duplicate customer records
duplicates = customers_df.sample(25)

customers_df = pd.concat(
    [customers_df, duplicates],
    ignore_index=True
)

# Save raw customer data
customers_df.to_csv(
    "data/raw/customers_raw.csv",
    index=False
)

print("Raw customer data generated successfully!")

#########################################

#create transactions categories
categories = [
    "Groceries",
    "Transport",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Shopping"
]

categories_df = pd.DataFrame({"category_name": categories})

# Add inconsistent category names
bad_categories = pd.DataFrame({
    "category_name": [
        "Grocery",
        "Transprt",
        "Unknown Expense"
    ]
})

categories_df = pd.concat(
    [categories_df, bad_categories],
    ignore_index=True
)

# Save raw categories data
categories_df.to_csv(
    "data/raw/categories_raw.csv",
    index=False
)

print("Raw category data generated successfully!")

########################################

#create transactions data
transactions = []

valid_categories = [
    "Groceries",
    "Transport",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Shopping"
]

for transaction_id in range(1, 10001):
    transaction = {
        "transaction_id": transaction_id,
        "customer_id": random.randint(1, 1000),
        "transaction_date": (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 364))),
        "category_name": random.choice(valid_categories),
        "transaction_amount": round(random.uniform(10.0, 5000.0), 2)
    }

    transactions.append(transaction)

# convert to DataFrame and corrupt the dataset
transactions_df = pd.DataFrame(transactions)
# Introduce invalid customer IDs
invalid_customers = random.sample(range(len(transactions_df)), 50)
transactions_df.loc[invalid_customers, "customer_id"] = 99999

# Negative amounts (refunds or errors)
negative_rows = random.sample(range(len(transactions_df)), 30)
transactions_df.loc[negative_rows, "transaction_amount"] *= -1

# Zero-value transactions
zero_rows = random.sample(range(len(transactions_df)), 20)
transactions_df.loc[zero_rows, "transaction_amount"] = 0

# Future-dated transactions
future_rows = random.sample(range(len(transactions_df)), 25)
transactions_df.loc[future_rows, "transaction_date"] = (
    datetime(2035, 1, 1)
    + timedelta(days=random.randint(0, 365))
)

# Missing dates
missing_rows = random.sample(range(len(transactions_df)), 15)
transactions_df.loc[missing_rows, "transaction_date"] = None

# Invalid categories
bad_categories = ["Crypto Gambling", "Unknown Fee", "System Error"]
bad_rows = random.sample(range(len(transactions_df)), 40)
transactions_df.loc[bad_rows, "category_name"] = random.choice(bad_categories)

# Duplicate transactions
duplicates = transactions_df.sample(30)
transactions_df = pd.concat(
    [transactions_df, duplicates],
    ignore_index=True
)

# Save raw transactions data
transactions_df.to_csv(
    "data/raw/transactions_raw.csv",
    index=False
)

print("Raw transaction data generated successfully!")