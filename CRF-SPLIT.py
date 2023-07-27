import os
import re
from PyPDF2 import PdfReader, PdfWriter
import tkinter as tk
from tkinter import filedialog
 
def extract_header_number(page_text):
    # Regular expression pattern to extract the 8-digit number from the first line
    pattern = r'(?<=AVIS DE DEBIT D\'OFFICE )\d{8}'
 
    match = re.search(pattern, page_text)
    if match:
        return match.group()
    else:
        return None
 
def split_pdf_by_header_number(input_file, output_dir):
    pdf_reader = PdfReader(input_file)
    total_pages = len(pdf_reader.pages)
 
    for page_num in range(total_pages):
        pdf_writer = PdfWriter()
        page = pdf_reader.pages[page_num]
        pdf_writer.add_page(page)
 
        page_text = page.extract_text()
        first_line = page_text.split('\n')[0]  # Get the first line of the page
        header_number = extract_header_number(first_line)
 
        if header_number:
            output_filename = os.path.join(output_dir, f"{header_number}.pdf")
        else:
            output_filename = os.path.join(output_dir, f"page_{page_num + 1}.pdf")
 
        with open(output_filename, 'wb') as output_file:
            pdf_writer.write(output_file)
 
def select_input_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
 
    file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf")])
    return file_path
 
if __name__ == "__main__":
    input_pdf_file = select_input_file()
   
    if not input_pdf_file:
        print("No file selected. Exiting.")
    else:
        current_directory = os.getcwd()
        output_directory = os.path.join(current_directory, "output_pages")
       
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
       
        split_pdf_by_header_number(input_pdf_file, output_directory)
        print("PDFs split successfully.")