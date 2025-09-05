from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import cv2
import os
import shutil
import pytesseract
import re
import easyocr
from pdf2image import convert_from_path



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

def refine_characterwise(tr_text, image_path):
    # Remove any "ROLL NUMBER:" or similar prefix
    tr_text = tr_text.upper().replace("^ROLL NUMBER:", "").replace("ROLL NUMBER:", "").replace("ROLLNUMBER:","").replace("^ROLLNUMBER:","").strip()
    print("tr_text: ", tr_text)

    scale = 1
    img_cv = cv2.imread(temp_image_path)
    img_cv_scaled = cv2.resize(img_cv, (0,0), fx=scale, fy=scale)
    img_with_box = img_cv_scaled.copy() 
    cv2.rectangle(img_with_box, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box, 2px thick

    roll_crop = img_cv_scaled[y:y+h, x:x+w]
    # Tesseract preprocessing
    gray = cv2.cvtColor(roll_crop, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    tess_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789B'
    text_tess = pytesseract.image_to_string(thresh, config=tess_config).strip().upper()

    print("Tesseract: ", text_tess, "len ", len(text_tess) )
    
    # EasyOCR
    result_easy = reader.readtext(thresh)
    text_easy = ''.join([t[1].upper() for t in result_easy])

    text_easy = text_easy.upper().replace("ROLL NUMBER:", "").replace("ROLL NUMBER:", "").strip()


    print("Easy OCR: ", text_easy, "len ", len(text_easy))


    text_tess = refine_roll(text_tess)
    text_easy = refine_roll(text_easy)

    print("Tesseract Refined: ", text_tess, "len ", len(text_tess) )
    print("Easy OCR Refined: ", text_easy, "len ", len(text_easy))

    # Ensure length at least 7
    tr_text = tr_text.ljust(7, '_')
    final_roll = []

    for idx, char in enumerate(tr_text[:7]):
        print("Char TrOCR: ", char)
        if idx == 0:
            final_roll.append(char if char == '2' else '2')
        elif idx == 1:
            final_roll.append(char if char in ['2','3'] else '_')
        elif idx == 2:
            final_roll.append('B' if char in ['B','R','8'] else 'B')
        else:
            if char in allowed_chars:
                final_roll.append(char)
            else:
                # candidates = []
                # if len(text_tess) > idx:
                #     candidates.append(text_tess[idx])
                # if len(text_easy) > idx:
                #     candidates.append(text_easy[idx])
                # picked = next((c for c in candidates if c in allowed_chars), '_')
                print("Char Tess: ", text_tess[idx], "Char easy: ", text_easy[idx])
                if text_tess[idx] != text_easy[idx]:
                    final_roll.append('_')
                else:
                    final_roll.append(text_tess[idx])
        print("final roll: ", final_roll)
    return ''.join(final_roll)


# Load pre-trained TrOCR model and processor
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")

input_folder = "quiz1"
temp_folder = "temp_images"
output_folder = "quiz1_renamed_Final"

os.makedirs(temp_folder, exist_ok=True)
os.makedirs(output_folder,exist_ok = True)

x, y, w, h = 1065, 560, 563, 123 # Coordinates for roll number

pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

reader = easyocr.Reader(['en'])
allowed_chars = set("0123456789B")

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

    pixel_values = processor(images=roll_crop, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].replace(" ","")

    print("Extracted Text:", generated_text)

    final_roll = refine_characterwise (generated_text, temp_image_path)

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

