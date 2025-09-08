#Run this from inside images folder

import os
import csv

input_folder = "."
output_csv = "submissions.csv"

question_to_page = {
    1: 1, 2: 1, 3: 1, 4: 1,   
    5: 2, 6: 2, 7: 2, 8: 2    
    #Need to handle subpage mapping
}

rows = []

for filename in sorted(os.listdir(input_folder)):

    if "_page" in filename:
        continue
        
    valid_extensions = {".png", ".jpg", ".jpeg"}
    name, extension = os.path.splitext(filename)
    if extension.lower() not in valid_extensions:
        continue

    name, extension = os.path.splitext(filename)

    parts = name.split("_")

    roll_number = parts[0]
    question_number = parts[1] if len(parts) > 1 else ""
    sub_question = parts[2] if len(parts) > 2 else ""

    print("Roll number: ", roll_number, "question_number: ", question_number, "sub_question: ", sub_question)
    print(type(question_number))

    file_path = filename
    page_number = question_to_page.get(int(question_number), None)
    print("Page number: ", page_number)
    print(type(page_number))
    page_path = f"{roll_number}_page{page_number}.png" if page_number else ""

    print("File path: ", file_path)
    print("Page path: ", page_path)

    response = f"{file_path};{page_path}"

    rows.append([roll_number, question_number, sub_question, response])


with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Roll Number", "Question Number", "Sub Question", "Response"])
    writer.writerows(rows)

print(f"CSV file saved as {output_csv}")
