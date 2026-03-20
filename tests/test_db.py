import sqlite3

conn = sqlite3.connect("db/retail.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM retail_data LIMIT 5")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()