#Run this from inside images folder

import os
import csv
import shutil

input_folder = "quiz1_images"
output_csv = os.path.join(input_folder,"submissions.csv")

#Make sure all question_to_page mappings are present
question_to_page = {
    1: 1, 2: 1, 3: 1, 4: 1,   
    5: 2, 6: 2, 7: 2, 8: 2    
    #Need to handle subpage mapping
}

rows = []
page_usage_count = {}

for filename in sorted(os.listdir(input_folder)):

    if "_page" in filename:
        continue
        
    valid_extensions = {".png", ".jpg", ".jpeg"}
    name, extension = os.path.splitext(filename)
    if extension.lower() not in valid_extensions:
        continue

    parts = name.split("_")

    roll_number = parts[0].strip()
    question_number = parts[1].strip() if len(parts) > 1 else ""
    sub_question = parts[2].strip() if len(parts) > 2 else ""

    print("Roll number: ", roll_number, "question_number: ", question_number, "sub_question: ", sub_question)
    print(type(question_number))

    file_path = filename
    page_number = question_to_page.get(int(question_number), None)
    print("Page number: ", page_number)
    print(type(page_number))
    page_path = f"{roll_number}_page{page_number}.png" if page_number else ""

    print("File path: ", file_path)
    print("Page path: ", page_path)

    if page_path: 
        relative_page_path = os.path.join(input_folder,page_path) #required to make copies of the page

        page_usage_count.setdefault(page_path,0)
        page_usage_count[page_path] += 1

        if (page_usage_count[page_path] > 1) : 
            new_filename, new_extension = os.path.splitext(page_path)
            new_page_path = f"{new_filename}_copy{page_usage_count[page_path] - 1}{new_extension}"
            new_page_fullpath = os.path.join(input_folder, new_page_path)

            if os.path.exists(relative_page_path):
                shutil.copy(relative_page_path,new_page_fullpath)
            
            page_path = new_page_path
    
    response = f"{file_path},{page_path}"

    reason_text = ""
    
    rows.append([roll_number, question_number, sub_question, reason_text, response])

with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["roll_num", "ques_num", "sub_ques", "reason_text","response"])
    writer.writerows(rows)
print(f"CSV file saved as {output_csv}")
