from app.ai.text_to_sql import generate_sql
from app.db.run_query import execute_sql

question = "Top selling products in Chennai"

sql_query = generate_sql(question)
print("Generated SQL:\n", sql_query)

# 🗄 Execute SQL
results = execute_sql(sql_query)

print("\nResults:")
for r in results:
    print(r)