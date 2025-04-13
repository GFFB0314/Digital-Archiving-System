import sqlite3
import os

# Adjust the path if needed; this assumes archive.db is in the same directory as this script
db_path = os.path.join(os.path.dirname(__file__), "archive.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get column names
cursor.execute("PRAGMA table_info(archives)")
columns = [col[1] for col in cursor.fetchall()]  # Get column names

# Fetch all records
cursor.execute("SELECT * FROM archives")
records = cursor.fetchall()

# Convert each row into a dictionary, EXCLUDING 'pdf_data'
records_as_dicts = [
    {col: value for col, value in zip(columns, row) if col != "pdf_data"} for row in records
]

# Print results without 'pdf_data'
for record in records_as_dicts:
    print(record)

conn.close()
