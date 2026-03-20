from app.ai.text_to_sql import generate_sql

question = "Top 5 products by revenue"

sql_query = generate_sql(question)

print("Generated SQL:\n", sql_query)