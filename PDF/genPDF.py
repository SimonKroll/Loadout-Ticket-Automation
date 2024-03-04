from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from datetime import datetime

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
            c.drawString(400, 675-offset, "Not An Official Scale Ticket")

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

        #dashes = 30
        #for dash in range(dashes):
        #    c.line(10+ dash*612/dashes,5.5*inch,dash*612/dashes +20, 5.5*inch)

        # Save the canvas to the PDF file
        c.save()

if __name__ == "__main__":
    # Example data
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Specify the output PDF file path
    output_path = 'output_report.pdf'

    # Generate the report
    generate_report(output_path, report_data)

    print(f"Report generated and saved to {output_path}")
