#For some pdfs first page and second page are swapped
#Currently works only for 2 pages.

from PyPDF2 import PdfReader, PdfWriter
import os

input_folder = "quiz1_pdfs"
output_folder = "quiz1_swapped_pdfs"
os.makedirs(output_folder,exist_ok = True)

input_pdfs = [] # Add pdfs which need pages swapped here. 

for pdf in input_pdfs:
    input_pdf = os.path.join(input_folder,pdf)
    output_pdf = os.path.join(output_folder,pdf)
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    writer.add_page(reader.pages[1]) 
    writer.add_page(reader.pages[0])
    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"Saved swapped PDF as {output_pdf}")