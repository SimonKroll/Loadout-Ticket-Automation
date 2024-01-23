from PDF import genPDF
from db import initalizeDB
from utilities import Buzzer

import os
import sqlite3
from datetime import datetime
from mfrc522 import SimpleMFRC522
#from RFID import read


# System Parameters
db_path = "./loadout(TESTING).db"
report_path = "./output_files/"


# On START
initalizeDB.initalize(db_path)

conn = sqlite3.connect(database=db_path)
cursor = conn.cursor()

report_data = genPDF.report_data

buzzer = Buzzer()
reader = SimpleMFRC522()

# RUN
while True:
    try:
        id, text = reader.read()
        buzzer.beep()


        cursor.execute("SELECT * FROM credentials WHERE CardID=?", [int(id)]) 
        row = cursor.fetchone() #TODO: Check that the card is on file before proceededing

        # Update & Retrieve the Ticket Counter
        cursor.execute("UPDATE counters SET value = value + 1 WHERE counter_name = 'loadID'") # TODO: Rename loadID to ticket
        conn.commit() 
        cursor.execute("SELECT value FROM counters WHERE counter_name = 'loadID';")
        ticket_number = str(cursor.fetchone()[0]).zfill(5)

        # Update & Retrieve the Contract Load Counter
        # TODO: initialize contract counters on startup
        cursor.execute('''INSERT OR IGNORE INTO counters
                          VALUES (?, 0)''', [row[6]])
        conn.commit() 

        cursor.execute("UPDATE counters SET value = value + 1 WHERE counter_name = ?", [row[6]])
        conn.commit() 
        cursor.execute("SELECT value FROM counters WHERE counter_name = ?", [row[6]])
        contract_load_number = str(cursor.fetchone()[0]).zfill(5)


        # Fill Report Data
        report_data = {
        'source_name': row[1],
        'source_address': row[2],
        'source_address_2': row[3],
        'source_phone': row[4],
        'ticket_number': ticket_number,
        'date' : datetime.now().strftime('%B %d, %Y'),
        'commodity': row[5],
        'contract_number' : row[6],
        'load_number' : contract_load_number,
        'customer_name': row[7],
        'customer_address': row[8],
        'customer_address_2': row[9],
        'customer_city_state': "", #row[10], # TODO: Determine if this is needed
        'carrier_name' : row[11],
        'truck_plate' : row[12],
        'trailer_plate' : row[13]
        }

    finally:
        pass

    # Generate the report
    output_file = report_path + f"Report_{datetime.now().strftime('%Y%m%d')}_{ticket_number}.pdf"
    genPDF.generate_report(output_file, report_data)

    # Print the report
    print(f"Report generated and saved to {output_file}")
    os.system(f"lp -d HP_Officejet_Pro_8600 {output_file}")

