import sqlite3
import csv
import os

conn = sqlite3.connect('./db/LoadoutCreds.db')
cursor = conn.cursor()

cursor.execute("select * from credentials")
with open("card_data.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=",")
    csv_writer.writerow([i[0] for i in cursor.description]) #prints the titles in the top row
    csv_writer.writerows(cursor)

dirpath = os.getcwd() + "/card_data.csv"
print ("Data exported Successfully into {}".format(dirpath))