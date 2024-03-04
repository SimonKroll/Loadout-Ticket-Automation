from PDF import genPDF
from db import initalizeDB
from utilities import Buzzer

import os
import sqlite3
import csv
from datetime import datetime
from mfrc522 import SimpleMFRC522
import time
#from RFID import read

# Get the absolute path of the script's directory
proj_dir = os.path.dirname(os.path.abspath(__file__))

### System Parameters
db_path = os.path.join(proj_dir,"loadout(TESTING).db")  #TODO: change to live DB
report_path = os.path.join(proj_dir,"output_files/reports/")
ticket_log = os.path.join(proj_dir,"output_files/log/load_history.csv")
# TODO: add error log path and logging functionality

# On START
initalizeDB.initalize(db_path)

conn = sqlite3.connect(database=db_path)
cursor = conn.cursor()

if not os.path.isfile(ticket_log):
    cursor.execute("select * from credentials")
    with open(ticket_log, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(["Timestamp", "Ticket #", "Contract Load #"]+[i[0] for i in cursor.description]) #prints the titles in the top row

report_data = genPDF.report_data

buzzer = Buzzer()
reader = SimpleMFRC522()
last_scan_time = datetime.now()

#Startup Sound
for _ in range(2):
    buzzer.beep(repetitions=3, duration=0.1, pause=0.05)
    buzzer.beep(duration=0.3, pause=0.05)
    buzzer.beep(duration=0.2, pause=0.2)

# RUN
while True:
    try:
        id, text = reader.read_no_block()
        
        if id and (datetime.now() - last_scan_time).total_seconds() > 15:
            last_scan_time = datetime.now()
            buzzer.beep()

            cursor.execute("SELECT * FROM credentials WHERE CardID=?", [int(id)]) 
            row = cursor.fetchone()

            if row: # Ensures card is on file
                # Update & Retrieve the Ticket Counter
                if (str(id) == "423312773588"): ## Sample ID for training, non-incrementing
                    ticket_number = "00000"
                    contract_load_number = "12345"
                else:
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
                'date' : datetime.now().strftime('%B %d, %Y %I:%M %p'),
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

                # Generate the report
                output_file = report_path + f"Report_{datetime.now().strftime('%Y%m%d')}_{ticket_number}.pdf"
                genPDF.generate_report(output_file, report_data)

                # Print the report
                os.system(f"lp -d HP_Officejet_Pro_8600 {output_file}")

                # TODO: create history logging function separately, consider using openpyxl?
                # Log the report
                with open(ticket_log, "a") as csv_file: 
                    csv_writer = csv.writer(csv_file, delimiter=",") # NOTE: use DictWriter for header support and better row definition 
                    csv_writer.writerow([datetime.now().strftime('%m/%d/%Y %I:%M:%S %p'), ticket_number, contract_load_number]+[ i for i in row]) #prints the titles in the top row
            else: # Card is not on file, log the error 
                pass

    except Exception as e:
        pass
    else:
        pass
    finally:
        pass



    


