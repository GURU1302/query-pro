import pandas as pd
import sqlite3

# Load Excel file into a DataFrame
excel_file = './clothing data.xlsx'  # Update with your Excel file path
df = pd.read_excel(excel_file)

# SQLite database file
db_file = 'review.db'  # Update with your desired database file path

# Establish connection to SQLite database
conn = sqlite3.connect(db_file)

# Write DataFrame to SQLite database
df.to_sql('REVIEW', conn, if_exists='replace', index=False)

# Commit changes and close connection
conn.commit()
conn.close()

print("Dataset imported into SQLite database successfully!")