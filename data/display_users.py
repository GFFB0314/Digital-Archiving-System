""""
import sqlite3
import os

# Adjust the path if needed; this assumes archive.db is in the same directory as this script
db_path = os.path.join(os.path.dirname(__file__), "archive.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get column names for the 'users' table
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]  # Get column names

# Fetch all records from the 'users' table
cursor.execute("SELECT * FROM users")
records = cursor.fetchall()

# Convert each row into a dictionary, EXCLUDING 'password' for security
records_as_dicts = [
    {col: value for col, value in zip(columns, row) if col.lower() != "password"} for row in records
]

# Print results without 'password'
for record in records_as_dicts:
    print(record)

conn.close()
"""

import sqlite3
import os

# Adjust the path if needed; this assumes archive.db is in the same directory as this script
db_path = os.path.join(os.path.dirname(__file__), "archive.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get column names for the 'users' table
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]  # Get column names

# Fetch all records from the 'users' table
cursor.execute("SELECT * FROM users")
records = cursor.fetchall()

# Convert each row into a dictionary (including 'password')
records_as_dicts = [
    {col: value for col, value in zip(columns, row)} for row in records
]

# Print results including 'password'
for record in records_as_dicts:
    print(record)

conn.close()
