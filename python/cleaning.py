import pandas as pd

##load raw data
#customers_df = pd.read_csv("data/raw/customers_raw.csv")
#categories_df = pd.read_csv("data/raw/categories_raw.csv")
#transactions_df = pd.read_csv("data/raw/transactions_raw.csv")
#print("Raw data loaded.")

##remove duplicate customers
#customers_before = len(customers_df)
#customers_df = customers_df.drop_duplicates()
#customers_after = len(customers_df)
#print(f"Removed {customers_before - customers_after} duplicate customers.")

##fix missing customer names
#customers_df["customer_name"] = (customers_df["customer_name"].fillna("Unknown Customer"))

##fix missing age groups
#customers_df["age_group"] = (customers_df["age_group"].fillna("Unknown Age Group"))

##fix invalid regions

#valid_regions = [
#    "Western Cape",
 #   "Gauteng",
  #  "KwaZulu-Natal",
   # "Eastern Cape",
   # "Free State"
#]
#customers_df.loc[~customers_df["region"].isin(valid_regions),"region"] = "Unknown"

##save cleaned data
#customers_df.to_csv("data/processed/customers_clean.csv",index=False)
#print("Clean customers saved.")

################################################
##standardise column names
#transactions_df.columns = transactions_df.columns.str.strip()

##remove invalid customer references in transactions
#valid_customer_ids = set(customers_df["customer_id"])
#transactions_df = transactions_df[transactions_df["customer_id"].isin(valid_customer_ids)]

##fix transaction dates
#transactions_df["transaction_date"] = pd.to_datetime(transactions_df["transaction_date"],errors="coerce")

#transactions_df = transactions_df.dropna(subset=["transaction_date"])

##remove future dated transactions
#today = pd.Timestamp.today()
#transactions_df = transactions_df[transactions_df["transaction_date"] <= today]

##handle negative amounts
#transactions_df = transactions_df[transactions_df["transaction_amount"] > 0]

##fix invalid categories
#valid_categories = [
#    "Groceries",
#    "Transport",
#    "Utilities",
#    "Entertainment",
#    "Healthcare",
#    "Shopping"
#]

#transactions_df = transactions_df[transactions_df["category_name"].isin(valid_categories)]

##remove duplicate transactions
#transactions_df = transactions_df.drop_duplicates(subset=["transaction_id"])

##save cleaned transactions

#transactions_df.to_csv("data/processed/transactions_clean.csv",index=False)
#print("Clean transactions saved.")

#######################################################categories
## Remove duplicate categories
#categories_df = categories_df.drop_duplicates()

## Remove missing category names
#categories_df = categories_df.dropna(subset=["category_name"])

## Keep only valid categories
#valid_categories = [
#    "Groceries",
#    "Transport",
#    "Utilities",
#    "Entertainment",
#    "Healthcare",
#    "Shopping"
#]

#categories_df = categories_df[
#    categories_df["category_name"].isin(valid_categories)
#]

## Save cleaned categories
#categories_df.to_csv(
#    "data/processed/categories_clean.csv",
#    index=False
#)

#print("Clean categories saved.")


#########################################################################
#########################################################################
#CLEANER VERSION:
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

VALID_REGIONS = [
    "Western Cape",
    "Gauteng",
    "KwaZulu-Natal",
    "Eastern Cape",
    "Free State"
]

VALID_CATEGORIES = [
    "Groceries",
    "Transport",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Shopping"
]


# ============================================================
# LOAD RAW DATA
# ============================================================

customers_df = pd.read_csv(
    "data/raw/customers_raw.csv"
)

categories_df = pd.read_csv(
    "data/raw/categories_raw.csv"
)

transactions_df = pd.read_csv(
    "data/raw/transactions_raw.csv"
)

print("Raw data loaded.")
print()


# ============================================================
# CLEAN CUSTOMERS
# ============================================================

print("Cleaning customers...")

# Remove duplicate customers
customers_before = len(customers_df)

customers_df = customers_df.drop_duplicates()

customers_after = len(customers_df)

print(
    f"Removed {customers_before - customers_after} duplicate customers."
)


# Fix missing customer names
missing_names = customers_df["customer_name"].isna().sum()

customers_df["customer_name"] = (
    customers_df["customer_name"]
    .fillna("Unknown Customer")
)

print(
    f"Fixed {missing_names} missing customer names."
)


# Fix missing age groups
missing_age_groups = customers_df["age_group"].isna().sum()

customers_df["age_group"] = (
    customers_df["age_group"]
    .fillna("Unknown Age Group")
)

print(
    f"Fixed {missing_age_groups} missing age groups."
)


# Fix invalid regions
invalid_regions = (
    ~customers_df["region"].isin(VALID_REGIONS)
).sum()
customers_df.loc[
    ~customers_df["region"].isin(VALID_REGIONS),
    "region"
] = "Unknown"
print(
    f"Fixed {invalid_regions} invalid regions."
)


# Save cleaned customers
customers_df.to_csv(
    "data/processed/customers_clean.csv",
    index=False
)
print(
    f"Clean customers saved: {len(customers_df)} customers."
)
print()


# ============================================================
# CLEAN TRANSACTIONS
# ============================================================

print("Cleaning transactions...")
# Standardise column names
transactions_df.columns = (
    transactions_df.columns
    .str.strip()
)


# ------------------------------------------------------------
# Remove invalid customer references
# ------------------------------------------------------------

valid_customer_ids = set(
    customers_df["customer_id"]
)
before = len(transactions_df)
transactions_df = transactions_df[
    transactions_df["customer_id"].isin(valid_customer_ids)
]
after = len(transactions_df)
print(
    f"Removed {before - after} transactions "
    f"with invalid customer IDs."
)


# ------------------------------------------------------------
# Convert transaction dates
# ------------------------------------------------------------

transactions_df["transaction_date"] = pd.to_datetime(
    transactions_df["transaction_date"],
    errors="coerce"
)


# ------------------------------------------------------------
# Remove missing transaction dates
# ------------------------------------------------------------

before = len(transactions_df)
transactions_df = transactions_df.dropna(
    subset=["transaction_date"]
)
after = len(transactions_df)
print(
    f"Removed {before - after} transactions "
    f"with missing dates."
)


# ------------------------------------------------------------
# Remove future-dated transactions
# ------------------------------------------------------------

today = pd.Timestamp.today().normalize()
before = len(transactions_df)
transactions_df = transactions_df[
    transactions_df["transaction_date"] <= today
]
after = len(transactions_df)
print(
    f"Removed {before - after} future-dated transactions."
)


# ------------------------------------------------------------
# Remove invalid transaction amounts
# ------------------------------------------------------------

before = len(transactions_df)
transactions_df = transactions_df[
    transactions_df["transaction_amount"] > 0
]
after = len(transactions_df)
print(
    f"Removed {before - after} transactions "
    f"with invalid amounts."
)


# ------------------------------------------------------------
# Remove invalid categories
# ------------------------------------------------------------

before = len(transactions_df)
transactions_df = transactions_df[
    transactions_df["category_name"].isin(
        VALID_CATEGORIES
    )
]
after = len(transactions_df)
print(
    f"Removed {before - after} transactions "
    f"with invalid categories."
)


# ------------------------------------------------------------
# Remove duplicate transactions
# ------------------------------------------------------------

before = len(transactions_df)
transactions_df = transactions_df.drop_duplicates(
    subset=["transaction_id"]
)
after = len(transactions_df)
print(
    f"Removed {before - after} duplicate transactions."
)
# Save cleaned transactions
transactions_df.to_csv(
    "data/processed/transactions_clean.csv",
    index=False
)
print(
    f"Clean transactions saved: "
    f"{len(transactions_df)} transactions."
)
print()


# ============================================================
# CLEAN CATEGORIES
# ============================================================

print("Cleaning categories...")
# Remove duplicate categories
before = len(categories_df)
categories_df = categories_df.drop_duplicates()
after = len(categories_df)
print(
    f"Removed {before - after} duplicate categories."
)


# Remove missing category names
before = len(categories_df)
categories_df = categories_df.dropna(
    subset=["category_name"]
)
after = len(categories_df)
print(
    f"Removed {before - after} categories "
    f"with missing names."
)
# Keep only valid categories
before = len(categories_df)
categories_df = categories_df[
    categories_df["category_name"].isin(
        VALID_CATEGORIES
    )
]
after = len(categories_df)
print(
    f"Removed {before - after} invalid categories."
)
# Save cleaned categories
categories_df.to_csv(
    "data/processed/categories_clean.csv",
    index=False
)
print(
    f"Clean categories saved: "    
    f"{len(categories_df)} categories."
)
print()

# ============================================================
# FINAL DATA QUALITY SUMMARY
# ============================================================
print("========================================")
print("DATA CLEANING COMPLETE")
print("========================================")
print(
    f"Customers:    {len(customers_df)}"
)
print(
    f"Categories:   {len(categories_df)}"
)
print(
    f"Transactions: {len(transactions_df)}"
)
print("========================================")
