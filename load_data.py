import pandas as pd
from sqlalchemy import create_engine

# Load CSV (from Kaggle)
df = pd.read_csv("superstore.csv", encoding="latin1")

# Clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Connect DB
engine = create_engine("postgresql+psycopg2://abhi:1234@127.0.0.1:5432/superstore")

# Load into PostgreSQL
df.to_sql("orders", engine, if_exists="replace", index=False)

print("Data loaded successfully!")