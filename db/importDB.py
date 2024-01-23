import sqlite3
import csv
import os

conn = sqlite3.connect('./db/LoadoutCreds.db')
cursor = conn.cursor()

# Open and read the CSV file
with open('card_data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Skip the header row
    ## TODO: Check if header is present
    next(csv_reader)

    values = ', '.join(['?' for _ in range(14)])
    # Insert data into the database
    for row in csv_reader:
        cursor.execute(f'''
            INSERT OR IGNORE INTO credentials 
            VALUES  ({values})''', row)
print("Data added!")
# Commit the changes and close the connection
conn.commit()
conn.close()