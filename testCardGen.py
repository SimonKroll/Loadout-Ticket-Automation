from PDF.genPDF import generate_report

from datetime import datetime
from mfrc522 import SimpleMFRC522
import os
import sqlite3
from utilities import Buzzer


if __name__ == "__main__":
    # Example data
    report_data = {
        'source_name': 'Source Name',
        'source_address': 'Source Address',
        'source_address_2': 'Source Address 2',
        'source_phone': 'Source Phone',
        'ticket_number': '00000',
        'date' : '01-01-2014',
        'commodity':'Soybean Meal',
        'contract_number' : '00000',
        'load_number' : '00000',
        'customer_name': 'Customer Name',
        'customer_address': 'Customer Address',
        'customer_address_2': 'Customer Address 2',
        'customer_city_state': 'City State Zip',
        'carrier_name' : 'Carrier Name',
        'truck_plate' : 'Truck License Plate',
        'trailer_plate' : 'Trailer License Plate'
    }

    #Set Buzzer
    buzzer = Buzzer()

    conn = sqlite3.connect('./db/LoadoutCreds.db')
    cursor = conn.cursor()

    # Specify the output PDF file path
    output_path = 'output_report.pdf'
    print("reader is live...")
    reader = SimpleMFRC522()

    try:
        id, text = reader.read()
        
        buzzer.beep()

        cursor.execute("SELECT * FROM credentials WHERE CardID=?", [int(id)]) 
        row = cursor.fetchone()
        report_data = {
        'source_name': row[1],
        'source_address': row[2],
        'source_address_2': row[3],
        'source_phone': row[4],
        'ticket_number': '00000',
        'date' : datetime.now().strftime('%B %d, %Y'),
        'commodity': row[5],
        'contract_number' : row[6],
        'load_number' : '00000',
        'customer_name': row[7],
        'customer_address': row[8],
        'customer_address_2': row[9],
        'customer_city_state': row[10],
        'carrier_name' : row[11],
        'truck_plate' : row[12],
        'trailer_plate' : row[13]
        }

    finally:
        pass

    # Generate the report
    generate_report(output_path, report_data)

    print(f"Report generated and saved to {output_path}")

    os.system("lp -d HP_Officejet_Pro_8600 output_report.pdf")
    print("printing...")
