import sqlite3
import json

# Connect to your SQLite DB
conn = sqlite3.connect('db.sqlite3-vps')
conn.row_factory = sqlite3.Row  # To get dict-like rows

cur = conn.cursor()

# List all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row['name'] for row in cur.fetchall() if row['name'] != 'sqlite_sequence']  # skip internal

all_data = {}

for table in tables:
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    all_data[table] = [dict(row) for row in rows]

# Save to JSON
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print("✅ Data exported to data.json")