import os
import cv2
from pdf2image import convert_from_path

input_folder = "quiz1_pdfs"
# temp_folder = "temp_images"
output_folder = "quiz1_images"
# os.makedirs(temp_folder,exist_ok = True)
os.makedirs(output_folder,exist_ok = True)

# # x, y, w, h = 0, 1103, 2457, 303 #Coordinates for question1
# # x, y, w, h = 0, 1096, 2476, 350
# #x, y, w, h = 0, 1393, 2476, 280 #Coordinates for question 2
# x, y, w, h = 0, 1376, 2476, 300

question_boundaries_page1 = {
    1: (0, 1096, 2480, 370),
    2: (0, 1376, 2480, 320),
    3: (0, 1640, 2480, 726),
    4: (0, 2266, 2480, 1240)
}

question_boundaries_page2 = {
    5: (0, 320, 2480, 890),
    6: (0, 1040, 2480, 1205),
    7: (0, 2105, 2480, 365),
    8: (15, 2350, 2480, 1156)
}

pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]

count =0
for pdf_file in pdf_files:
    pdf_path =os.path.join(input_folder,pdf_file)
    pages = convert_from_path(pdf_path,dpi = 300)
    first_page = pages[0]
    first_page_path = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_page1.png")
    first_page.save(first_page_path, "PNG")
    print("First Page saved")

    second_page = pages[1]
    second_page_path = os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_page2.png")
    second_page.save(second_page_path, "PNG")
    print("Second Page saved")

    scale = 1
    img_cv = cv2.imread(first_page_path)
    img_cv_scaled = cv2.resize(img_cv, (0,0), fx=scale, fy=scale)
    
    for q_num, (x,y,w,h) in question_boundaries_page1.items():

        img_with_box = img_cv_scaled.copy() 

        # cv2.rectangle(img_with_box, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box, 2px thick
        # cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_page_with_box.png"), img_with_box)
        
        question_crop = img_cv_scaled[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_{q_num}.png"), question_crop)
        print("Saved question ", q_num)

    scale = 1
    img_cv_2 = cv2.imread(second_page_path)
    img_cv_scaled_2 = cv2.resize(img_cv_2, (0,0), fx=scale, fy=scale)

    for q_num, (x,y,w,h) in question_boundaries_page2.items():

        img_with_box = img_cv_scaled_2.copy() 

        # cv2.rectangle(img_with_box, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green box, 2px thick
        # cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_page_with_box.png"), img_with_box)
        
        question_crop = img_cv_scaled_2[y:y+h, x:x+w]
        cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_{q_num}.png"), question_crop)
        print("Saved question ", q_num)

    print("Count ", count)
    count = count + 1


