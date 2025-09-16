import os
import cv2
from pdf2image import convert_from_path

input_folder = "quiz2_renamed_Final"
# temp_folder = "temp_images"
output_folder = "quiz2_images"
# os.makedirs(temp_folder,exist_ok = True)
os.makedirs(output_folder,exist_ok = True)

#   Format : x,y,w,h
#quiz1
# question_boundaries_page1 = {
#     1: (0, 1096, 2480, 370),
#     2: (0, 1376, 2480, 320),
#     3: (0, 1640, 2480, 726),
#     4: (0, 2266, 2480, 1240)
# }

# question_boundaries_page2 = {
#     5: (0, 320, 2480, 890),
#     6: (0, 1040, 2480, 1205),
#     7: (0, 2105, 2480, 365),
#     8: (15, 2350, 2480, 1156)
# }

#quiz2
question_boundaries_page1 = {
    1: {
        1: (0, 925, 2480, 1140),
        2: (0, 1960, 2480, 490),
        3: (0, 2370, 2480, 1106)   #You can get total width and height also from GetBoundaries
        }
}

question_boundaries_page2 = {
    2: (0, 0, 2480, 3506)
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
    
    for q_num, q_data in question_boundaries_page1.items():
        if isinstance(q_data, dict): 
            for subq_num, (x, y, w, h) in q_data.items():
                question_crop = img_cv_scaled[y:y+h, x:x+w]
                cv2.imwrite(os.path.join(output_folder,f"{os.path.splitext(pdf_file)[0]}_{q_num}_{subq_num}.png"),question_crop)
                print(f"Saved question {q_num}.{subq_num}")
        else: 
            x, y, w, h = q_data
            question_crop = img_cv_scaled[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_{q_num}.png"),question_crop)
            print(f"Saved question {q_num}")

    scale = 1
    img_cv_2 = cv2.imread(second_page_path)
    img_cv_scaled_2 = cv2.resize(img_cv_2, (0,0), fx=scale, fy=scale)

    for q_num, q_data in question_boundaries_page2.items():
        if isinstance(q_data, dict): 
            for subq_num, (x, y, w, h) in q_data.items():
                question_crop = img_cv_scaled_2[y:y+h, x:x+w]
                cv2.imwrite(os.path.join(output_folder,f"{os.path.splitext(pdf_file)[0]}_{q_num}_{subq_num}.png"),question_crop)
                print(f"Saved question {q_num}.{subq_num}")
        else: 
            x, y, w, h = q_data
            question_crop = img_cv_scaled_2[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(output_folder, f"{os.path.splitext(pdf_file)[0]}_{q_num}.png"),question_crop)
            print(f"Saved question {q_num}")

    print("Count ", count)
    count = count + 1


