import pandas as pd


# inspect dates
#transactions_df = pd.read_csv(
#    "data/processed/transactions_clean.csv"
#)

#print(transactions_df.head())

##print("\nColumns:")
#print(transactions_df.columns)

#convert dates
import pandas as pd

transactions_df = pd.read_csv(
    "data/processed/transactions_clean.csv"
)

# Convert the transaction_date column into real dates
transactions_df["transaction_date"] = pd.to_datetime(
    transactions_df["transaction_date"]
)

# Keep only unique dates
date_df = pd.DataFrame()

date_df["full_date"] = (
    transactions_df["transaction_date"]
    .drop_duplicates()
    .sort_values()
)
date_df = date_df.reset_index(drop=True)

#edit make more serious
# Create the warehouse key
date_df["date_id"] = (
    date_df["full_date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

# Extract useful reporting fields
date_df["day"] = date_df["full_date"].dt.day
date_df["month"] = date_df["full_date"].dt.month
date_df["month_name"] = date_df["full_date"].dt.month_name()
date_df["quarter"] = date_df["full_date"].dt.quarter
date_df["year"] = date_df["full_date"].dt.year
date_df["day_name"] = date_df["full_date"].dt.day_name()
date_df["is_weekend"] = (date_df["full_date"].dt.dayofweek >= 5) #day 6/7


#saveeee
date_df.to_csv(
    "data/processed/date_dimension.csv",
    index=False
)

print(date_df.head())
print()
print(f"Date dimension contains {len(date_df)} rows.")