import sqlite3
import re

def clean_sql(query):
    # Remove markdown code fences ```sql ... ```
    query = re.sub(r"```.*?```", lambda m: m.group(0).strip("`").replace("sql", ""), query, flags=re.DOTALL)

    # Remove any remaining backticks
    query = query.replace("```", "").replace("sql", "")

    return query.strip()


def execute_sql(query):

    query = clean_sql(query)

    conn = sqlite3.connect("database/retail.db")
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        results = f"SQL Error: {e}"

    conn.close()

    return results