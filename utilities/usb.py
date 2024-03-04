#!/usr/bin/python3

import os
import logging    # first of all import the module
import sys
import sqlite3
import csv
from Buzzer import Buzzer
import encoder

buzzer = Buzzer()

logging.basicConfig(filename='/home/pi/dev/Loadout-Ticket-Automation/utilities/log.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning(os.getcwd())
try:
    if len(sys.argv) > 1:
        buzzer.beep()

        drive_name = sys.argv[1]
        logging.warning(f"USB drive {drive_name} inserted. Running Python script...")

        drive_path = f"/dev/{drive_name}"  # Assuming the drive is mounted under /dev

        mount_path = "/home/pi/dev/Loadout-Ticket-Automation/usbmount/"
        output_path = mount_path+"LoadOutTicket/"
        project_path = "/home/pi/dev/Loadout-Ticket-Automation/"

        #db_file = project_path+'db/LoadoutCreds.db'
        db_file = project_path+'db/production.db'
        load_hist_file = project_path+ "output_files/log/load_history.csv"

        # mount the drive
        os.system(f"mount {drive_path} {mount_path}")

        #create folder
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        # Upload History log
        if os.path.isfile(load_hist_file):
            os.system(f" cp {load_hist_file} {output_path}")

        #TODO: check for file and read it into DB
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        logging.error("is File?  {}".format(os.path.isfile(output_path+"card_data.csv")))
        if os.path.isfile(output_path+"card_data.csv"):
            # Open and read the CSV file
            with open(output_path+'card_data.csv', 'r') as csv_file:
                csv_reader = csv.reader(csv_file)

                # Skip the header row
                ## TODO: Check if header is present
                next(csv_reader)

                values = ', '.join(['?' for _ in range(14)])
                # Insert data into the database
                for row in csv_reader:
                    cursor.execute(f'''
                        INSERT OR REPLACE INTO credentials 
                        VALUES  ({values})''', [encoder.id_decode(row[0])] + row[1:])
            # Commit the changes and close the connection
            conn.commit()
            conn.close()
            logging.warning(f"Data written to the DB")
            #TODO: When new data is added to DB, create new contract instance
        else:
            cursor.execute("select * from credentials")
            with open(output_path+"card_data.csv", "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow([i[0] for i in cursor.description]) #prints the titles in the top row
                #csv_writer.writerows(cursor)
                for row in cursor:
                    card_id = encoder.id_encode(row[0])
                    row = (card_id,) + row[1:]
                    csv_writer.writerow(row)

            dirpath = output_path + "card_data.csv"
            logging.warning("Data exported Successfully into {}".format(dirpath))


        #TODO: umount usb
        #
        os.system(f"umount {mount_path}")
except Exception as e:
    logging.error(e)


buzzer.beep(repetitions = 3, duration = 0.2, pause = 0.1)
