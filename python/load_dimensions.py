##########test the postgres connection

#from sqlalchemy import create_engine


#try:
#    with engine.connect() as connection:
#        print("Successfully connected to PostgreSQL!")
#except Exception as e:
#    print("Connection failed!")
#    print(e)


########updated code after connection test#######
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

customers_df = pd.read_csv("data/processed/customers_clean.csv")

###############test reading the CSV#############
#print(customers_df.head()) #this is annoying but it works, I guess. I will remove it later.
print("Loading customers...")




############Insert ONE customer#############################
#with engine.begin() as connection:

#    first_customer = customers_df.iloc[0]

#    connection.execute(
#        text("""
 #           INSERT INTO dim_customer
  #          (customer_id, customer_name, region, age_group)

   #         VALUES
    #        (:customer_id,
     ##       :region,
       #      :age_group)
        #"""),
#
 #       {
  #          "customer_id": int(first_customer["customer_id"]),
   ##        "region": first_customer["region"],
     #       "age_group": first_customer["age_group"]
      #  }

    #)

#print("One customer inserted.")


############gang customers now#############################


with engine.begin() as connection:
    ###clear tables firsy everytime
    connection.execute(text("""
    TRUNCATE TABLE
        dim_customer,
        dim_category,
        dim_date
    CASCADE;
    """))
    for _, customer in customers_df.iterrows():

        connection.execute(
            text("""
                INSERT INTO dim_customer
                (
                    customer_id,
                    customer_name,
                    region,
                    age_group
                )

                VALUES
                (
                    :customer_id,
                    :customer_name,
                    :region,
                    :age_group
                )
            """),
            {
                "customer_id": int(customer["customer_id"]),
                "customer_name": customer["customer_name"],
                "region": customer["region"],
                "age_group": customer["age_group"]
            }
        )

print(f"{len(customers_df)} customers loaded successfully!")
#print(f" Loaded {len(customers_df)} customers.")

################load categories now#############################
print("Loading categories...") #now it will look clean bro
categories_df = pd.read_csv(
    "data/processed/categories_clean.csv"
)

with engine.begin() as connection:

    for _, category in categories_df.iterrows():

        connection.execute(
            text("""
                INSERT INTO dim_category
                (category_id, category_name)

                VALUES
                (:category_id, 
                :category_name)
            """),
            {	
            	"category_id": int(category.name) + 1,
                "category_name": category["category_name"]
            }
        )

print(f"{len(categories_df)} categories loaded successfully!")


#################load dates ##########################
date_df = pd.read_csv(
    "data/processed/date_dimension.csv"
)
print("Loading dates...")

with engine.begin() as connection:

    for _, date in date_df.iterrows():

        connection.execute(
            text("""
                INSERT INTO dim_date
                (
                    date_id,
                    full_date,
                    day,
                    month,
                    quarter,
                    year
                )

                VALUES
                (
                    :date_id,
                    :full_date,
                    :day,
                    :month,
                    :quarter,
                    :year
                )
            """),
            {
                "date_id": int(date["date_id"]),
                "full_date": date["full_date"],
                "day": int(date["day"]),
                "month": int(date["month"]),
                "quarter": int(date["quarter"]),
                "year": int(date["year"])
            }
        )

print(f"{len(date_df)} dates loaded successfully!")
