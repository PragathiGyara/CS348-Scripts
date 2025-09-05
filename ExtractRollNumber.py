from pdf2image import convert_from_path
import cv2
import os
import pytesseract
import re
import easyocr
import shutil

def refine_roll(ocr_text):
    ocr_text = ''.join([c for c in ocr_text if c.isalnum()]).upper()
    final_roll = []

    if len(ocr_text) >= 1 and ocr_text[0] == '2':
        final_roll.append('2')
    else:
        final_roll.append('_')

    if len(ocr_text) >= 2 and ocr_text[1] in ['2', '3']:
        final_roll.append(ocr_text[1])
    else:
        final_roll.append('_')

    if len(ocr_text) >= 3 and ocr_text[2] == 'B':
        final_roll.append('B')
    else:
        final_roll.append('B')  # enforce 'B' if OCR missed

    # Last 4 digits
    last_digits = ''
    if len(ocr_text) > 3:
        for c in ocr_text[3:7]:
            if c.isdigit():
                last_digits += c
            else:
                last_digits += '_'
    # Pad with '_' if less than 4 digits
    last_digits = last_digits.ljust(4, '_')
    final_roll.extend(list(last_digits))

    return ''.join(final_roll)

input_folder = "quiz1"
temp_folder = "temp_images"
output_folder = "quiz1_renamed"

os.makedirs(temp_folder, exist_ok=True)
os.makedirs(output_folder,exist_ok = True)

x, y, w, h = 1065, 560, 563, 123 # Coordinates for roll number

pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

count =0
for pdf_file in pdf_files:
    pdf_path = os.path.join(input_folder, pdf_file)
    pages = convert_from_path(pdf_path,dpi = 300)
    first_page = pages[0]
    temp_image_path = os.path.join(temp_folder, f"{os.path.splitext(pdf_file)[0]}_page1.png")
    first_page.save(temp_image_path, "PNG")

    print("First Page extracted")


    scale = 1
    img_cv = cv2.imread(temp_image_path)
    img_cv_scaled = cv2.resize(img_cv, (0,0), fx=scale, fy=scale)
    img_with_box = img_cv_scaled.copy() 
    cv2.rectangle(img_with_box, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box, 2px thick

    roll_crop = img_cv_scaled[y:y+h, x:x+w]
    # cv2.imwrite(os.path.join("Temp_output_images", f"{os.path.splitext(pdf_file)[0]}_page_with_box.png"), img_with_box)
    # cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_roll_crop.png"), roll_crop)
    # print("Saved cropped roll number box as 'roll_crop.png'")

    tess_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=1234567890B'
    gray = cv2.cvtColor(roll_crop, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(thresh, config=tess_config).strip()
    print("Tesseract: ", text, "len: ", len(text))

    # match = re.search(r"\d{2}[A-Z]\d{4}", text)
    # if match:
    #     roll_tess = match.group()
    # else:
    #     roll_tess = "UNKNOWN"
    # print(f"Tesseract {pdf_path} -> {roll_tess}, {match} {text}")

    reader = easyocr.Reader(['en'])
    result = reader.readtext(thresh)
    text_easy = ''.join([t[1] for t in result]).strip()
    allowed_chars = set("0123456789B")
    text_easy = ''.join([c for c in text_easy if c in allowed_chars])
    print("Easy OCR: ", text_easy, "len: ", len(text_easy))


    text = refine_roll(text)
    text_easy = refine_roll(text_easy)

    # match_easy = re.search(r'2[23]B\d{4}', text_easy)
    # roll_easy = match_easy.group() if match_easy else "UNKNOWN"
    # print(f"[EASYOCR] {pdf_path} -> {roll_easy}, OCR Text: '{text_easy}'")


    if len(text) == 7 and len(text_easy) == 7:
        final_roll = list(text)  
        for idx in [1,3,4,5,6]:
            print("roll_tess: ", text[idx], "roll_tess: ", text_easy[idx])
            if text[idx] != text_easy[idx]:
                final_roll[idx] = '_'
        final_roll = ''.join(final_roll)
    else:
        final_roll = "UNKNOWN"

    print(f"Final roll number after comparison: {final_roll}")

    new_pdf_name = f"{final_roll}.pdf"
    new_pdf_path = os.path.join(output_folder, new_pdf_name)
    counter = 1

    while os.path.exists(new_pdf_path):
        new_pdf_name = f"{final_roll}.{counter}.pdf"
        new_pdf_path = os.path.join(output_folder, new_pdf_name)
        counter += 1

    shutil.copy(pdf_path, new_pdf_path)
    print("Pdf ", count, "copied")
    count = count + 1



