import os

def get_last_report(report_folder_path):

    pdf_files = [file for file in os.listdir(report_folder_path) if file.endswith('.pdf')]

    most_recent_file = max((os.path.join(report_folder_path, pdf_file) for pdf_file in pdf_files), key=os.path.getmtime, default=None)

    if most_recent_file:
        print(f"\nThe most recently created or modified PDF file is: {most_recent_file}\n")
        return most_recent_file
    else:
        print("No PDF files found in the folder.")
        return None
    

if __name__ == '__main__':

    path = os.path.dirname(__file__)
    recent_file = get_last_report(path)