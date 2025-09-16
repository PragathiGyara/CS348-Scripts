#Use rotate for 180 deg

from pdf2image import convert_from_path
from PIL import Image
import os
import fitz

input_folder = "quiz2_renamed_Final"
output_folder = "quiz2_flipped_pdfs"
os.makedirs(output_folder,exist_ok = True)

input_pdfs = ["2_B____.1.pdf"] 

# def flip_pdf_x_images(input_path, output_path):
#     input_path = os.path.join(input_folder,i)
#     output_path = os.path.join(output_folder,i)
#     pages = convert_from_path(input_path, dpi=300)
#     flipped_pages = []
#     for page in pages:
#         flipped = page.transpose(Image.FLIP_LEFT_RIGHT)  # horizontal flip
#         flipped_pages.append(flipped)
#     flipped_pages[0].save(output_path, save_all=True, append_images=flipped_pages[1:])

def rotate(i):
    input_path = os.path.join(input_folder,i)
    output_path = os.path.join(output_folder,i)
    doc = fitz.open(input_path)
    for page in doc:
        page.set_rotation(180) 
    doc.save(output_path)

for i in input_pdfs:
    # flip_pdf_x_images(i,i)
    rotate(i)


