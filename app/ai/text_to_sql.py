import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv("config/.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SCHEMA = """
Table: retail_data

Columns:
District
City
Store_ID
Store_Type
Product_Name
Category
Brand
Units_Sold
Revenue
Profit
Price
Stock_Level
Reorder_Level
Supplier
Delivery_Time_Days
Order_Date
"""

def generate_sql(question):

    prompt = f"""
You are an expert SQL generator.

{SCHEMA}

Convert the following question into a valid SQLite SQL query.
Return ONLY the SQL query. No explanation.

Question: {question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()