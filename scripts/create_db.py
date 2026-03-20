import pandas as pd
import sqlite3

df = pd.read_csv("data/retail_data.csv")

df.columns = [col.strip().replace(" ", "_") for col in df.columns]

conn = sqlite3.connect("database/retail.db")

df.to_sql("retail_data", conn, if_exists="replace", index=False)

conn.close()

print("Retail database created successfully!")
print("Columns:", df.columns.tolist())