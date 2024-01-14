from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from datetime import datetime
from mfrc522 import SimpleMFRC522
import os
import sqlite3
from utilities import Buzzer

def generate_report(output_path, report_data):
    # Create a new PDF file
    with open(output_path, 'wb') as output_file:
        # Use the template PDF as a canvas
        c = canvas.Canvas(output_file, pagesize=letter)

        for i in range(2):
            offset = i* 5.5*inch
            # Set font and size
            c.setFont("Helvetica-Bold", 11)

            c.drawCentredString(4.25*inch,720-offset, "OUTBOUND")

            # Set font and size
            c.setFont("Helvetica", 11)

            # Draw form elements
            c.drawString(72, 705-offset, f"{report_data['source_name']}")
            c.drawString(72, 690-offset, f"{report_data['source_address']}")
            c.drawString(72, 675-offset, f"{report_data['source_address_2']}")
            c.drawString(72, 660-offset, f"{report_data['source_phone']}")

            # Draw date and Ticket #
            c.drawString(400, 705-offset, f"Loadout Ticket # {report_data['ticket_number']}")
            c.drawString(400, 690-offset, f"Date: {report_data['date']}")
            c.drawString(400, 675-offset, "Not An Official Scale Ticket")


            c.drawString(72, 630-offset, f"Commodity: {report_data['commodity']}")

            c.drawString(300, 600-offset, f"Contract #: {report_data['contract_number']}")
            c.drawString(300, 585-offset, f"Load # on Contract: {report_data['load_number']}")
            
            c.drawString(72, 600-offset, "Customer:")
            c.drawString(72, 585-offset, f"{report_data['customer_name']}")
            c.drawString(72, 570-offset, f"{report_data['customer_address']}")
            c.drawString(72, 555-offset, f"{report_data['customer_address_2']}")
            c.drawString(72, 540-offset, f"{report_data['customer_city_state']}")

            c.drawString(72, 510-offset, f"Carrier: {report_data['carrier_name']}")
            c.drawString(72, 495-offset, f"Truck License Plate: {report_data['truck_plate']}")
            c.drawString(72, 480-offset, f"Trailer License Plate: {report_data['trailer_plate']}")

        dashes = 30
        for dash in range(dashes):
            c.line(10+ dash*612/dashes,5.5*inch,dash*612/dashes +20, 5.5*inch)

        # Save the canvas to the PDF file
        c.save()

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
