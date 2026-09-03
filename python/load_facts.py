#libraries bro
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

################ Create a connection to the PostgreSQL database ############################
#engine ...(this had a PASSWORD leak)
################ read cleaned transactions data ###########################
transactions_df = pd.read_csv("data/processed/transactions_clean.csv")
print("Loading transactions...")
#print(transactions_df.head())

################ read lookup tables from sql #########################

customers_df = pd.read_sql("SELECT customer_id FROM dim_customer",engine)
categories_df = pd.read_sql("SELECT category_id, category_name FROM dim_category",engine)
dates_df = pd.read_sql("SELECT date_id, full_date FROM dim_date",engine)

print()  #confirmation of data loaded
print(f"Transactions: {len(transactions_df)}")
print(f"Customers: {len(customers_df)}")
print(f"Categories: {len(categories_df)}")
print(f"Dates: {len(dates_df)}")

#merge
transactions_df = transactions_df.merge(categories_df, on = "category_name", how = "left")
print("\nAfter category lookup:")
print(
    transactions_df[["transaction_id", "category_name", "category_id"]].head()
)


###############
transactions_df["transaction_date"] = pd.to_datetime(
    transactions_df["transaction_date"]
)

dates_df["full_date"] = pd.to_datetime(
    dates_df["full_date"]
)

transactions_df = transactions_df.merge(
    dates_df,
    left_on="transaction_date",
    right_on="full_date",
    how="left"
)

#look at the result
print("\nAfter date lookup:")

print(
    transactions_df[
        [
            "transaction_id",
            "transaction_date",
            "date_id"
        ]
    ].head()
)

################################fact table creation####################################
# Select columns for the fact table
fact_df = transactions_df[
    [
        "transaction_id",
        "customer_id",
        "date_id",
        "category_id",
        "transaction_amount"
    ]
].copy()


print("\nFact table preview:")
print(fact_df.head())
print()
print(f"Rows ready for fact table: {len(fact_df)}")

######
print(f"Rows ready for fact table: {len(fact_df)}")
# Clear existing fact table data
with engine.begin() as connection:
    connection.exec_driver_sql(
        "TRUNCATE TABLE fact_transactions;"
    )

print("\nLoading fact transactions...")

# Load fact data into PostgreSQL
fact_df.to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False
)

print(f"{len(fact_df)} fact transactions loaded successfully!")
