import os
import cv2
from pdf2image import convert_from_path
import shutil
import csv

input_folder = input("Enter the input folder path containing PDFs (according to Roll Number): ").strip()
output_folder = os.path.join(os.path.dirname(input_folder), "images")
os.makedirs(output_folder,exist_ok = True)

print("Output folder : " + output_folder)

output_csv = os.path.join(output_folder,"submissions.csv")


#Example 
# question_boundaries = {
#     1: {   # Page 1
#         1: {   # Question 1 with subquestions
#             1: (0, 925, 2480, 1140),
#             2: (0, 1960, 2480, 490),
#             3: (0, 2370, 2480, 1106),
#         },
#         2: (0, 120, 2480, 800)  # Question 2 without subquestions
#     },
#     2: {   # Page 2
#         3: (0, 0, 2480, 3506)
#     }
# }


# Quiz 2
# question_boundaries = {
#     1: { 
#         1: {  
#             1: (0, 925, 2480, 1140),
#             2: (0, 1960, 2480, 490),
#             3: (0, 2370, 2480, 1106)
#         }
#     },
#     2: {  
#         2: (0, 0, 2480, 3506)
#     }
# }
# question_to_page = {
#     (1, ""): 1, #Fallback
#     (1, "1"): 1, 
#     (1, "2"): 1,   
#     (1, "3"): 1,    
#     (2, ""): 2
# }

#MidSem
# question_boundaries = {
#     1: { 
#         1: (0, 945, 2480, 820),
#         2: (0, 1670, 2480, 395),
#         3: (0, 1995, 2480, 1526)
#     },
#     2: {  
#         4: (0, 535, 2480, 585),
#         5: (0, 1045, 2480, 920),
#         6: (0, 1860, 2480, 1646)
#     },
#     3: {
#         7: (0, 515, 2480, 1340),
#         8: {
#             1: (0, 1780, 2480, 1035)
#         }
#     },
#     4: {
#         8: {
#             2: (0, 515, 2480, 745)
#         },
#         9: (0, 1160, 2480, 2346)
#     }
# }

# question_to_page = {
#     (1, ""): 1,
#     (2, ""): 1, 
#     (3, ""): 1,   
#     (4, ""): 2,    
#     (5, ""): 2,
#     (6, ""): 2,
#     (7, ""): 3,
#     (8, "1"): 3,
#     (8, "2"): 4,
#     (9, ""): 4
# }

rows = []
page_usage_count = {}


def get_boundaries_from_user():
    question_boundaries={}
    question_to_page={}
    num_pages = int(input("Enter number of pages: ").strip())
    current_question_number = 1

    for page in range(1,num_pages+1):
        print(f"\n--- Page {page} ---")
        num_questions = int(input(f"Enter number of questions on page {page}: ").strip())
        question_boundaries[page] = {}

        for _ in range(1, num_questions + 1):
            q = int(input("\n Enter question number: "))
            print(f"\nQuestion {q}:")
            has_sub = input("Does this question have subquestions? (y/n): ").strip().lower() == 'y'

            if has_sub:
                question_boundaries[page][q] = {}
                num_sub = int(input("Enter number of subquestions: ").strip())
                for s in range(1, num_sub + 1):
                    print(f"Subquestion {s}:")
                    x = int(input("  Enter x: ").strip())
                    y = int(input("  Enter y: ").strip())
                    w = int(input("  Enter width (w): ").strip())
                    h = int(input("  Enter height (h): ").strip())
                    question_boundaries[page][q][s] = (x, y, w, h)
                    question_to_page[(q, str(s))] = page


            else:
                x = int(input("  Enter x: ").strip())
                y = int(input("  Enter y: ").strip())
                w = int(input("  Enter width (w): ").strip())
                h = int(input("  Enter height (h): ").strip())
                question_boundaries[page][q] = (x, y, w, h)
                question_to_page[(q, "")] = page
            current_question_number += 1

    print("\nBoundaries collected successfully.")
    return question_boundaries, question_to_page


def getCSV(question_to_page):
    for filename in sorted(os.listdir(output_folder)):

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
        q_key = (int(question_number), sub_question)
        page_number = question_to_page.get(q_key)

        # Fallback if not found (maybe no subquestion mapping, just use question number)
        if page_number is None:
            page_number = question_to_page.get((int(question_number), ""))

        print("Page number: ", page_number)
        print(type(page_number))
        page_path = f"{roll_number}_page{page_number}.png" if page_number else ""

        print("File path: ", file_path)
        print("Page path: ", page_path)

        if page_path: 
            relative_page_path = os.path.join(output_folder,page_path) #required to make copies of the page

            page_usage_count.setdefault(page_path,0)
            page_usage_count[page_path] += 1

            if (page_usage_count[page_path] > 1) : 
                new_filename, new_extension = os.path.splitext(page_path)
                new_page_path = f"{new_filename}_copy{page_usage_count[page_path] - 1}{new_extension}"
                new_page_fullpath = os.path.join(output_folder, new_page_path)

                if os.path.exists(relative_page_path):
                    shutil.copy(relative_page_path,new_page_fullpath)
                
                page_path = new_page_path
        
        response = f"{file_path},{page_path}"

        reason_text = ""

        rows.append([roll_number,question_number,sub_question,reason_text,response])

    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["roll_num","ques_num","sub_ques","reason_text","response"])
        writer.writerows(rows)
    print(f"CSV file saved as {output_csv}")


def getImages(question_boundaries):
    pdf_files = sorted(f for f in os.listdir(input_folder) if f.lower().endswith('.pdf'))

    for count, pdf_file in enumerate(pdf_files):
        pdf_path =os.path.join(input_folder,pdf_file)
        pages = convert_from_path(pdf_path,dpi = 300)

        roll_number = os.path.splitext(pdf_file)[0]


        for page_index,page in enumerate(pages,start =1):
            page_path = os.path.join(output_folder,f"{roll_number}_page{page_index}.png")
            page.save(page_path,"PNG")
            print(f"Page {page_index} for {roll_number} saved")

            if page_index not in question_boundaries:
                continue

            scale =1
            img_cv = cv2.imread(page_path)
            img_cv_scaled = cv2.resize(img_cv, (0,0), fx=scale, fy=scale)

            for q_num, q_data in question_boundaries[page_index].items():
                if isinstance(q_data, dict):  # subquestions
                    for subq_num, (x, y, w, h) in q_data.items():
                        question_crop = img_cv_scaled[y:y+h, x:x+w]
                        out_path = os.path.join(output_folder, f"{roll_number}_{q_num}_{subq_num}.png")
                        cv2.imwrite(out_path, question_crop)
                        print(f"Saved question {q_num}.{subq_num}")

                else:  # single question
                    x, y, w, h = q_data
                    question_crop = img_cv_scaled[y:y+h, x:x+w]
                    out_path = os.path.join(output_folder, f"{roll_number}_{q_num}.png")
                    cv2.imwrite(out_path, question_crop)
                    print(f"Saved question {q_num}")
                
        print("Processed file count:", count + 1)

def main():
    question_boundaries, question_to_page = get_boundaries_from_user()

    print("\n Question Boundaries: ")
    print(question_boundaries)

    print("\n\n Question to page mapping: ")
    print(question_to_page)

    getImages(question_boundaries)
    getCSV(question_to_page)

if __name__ == "__main__":
    main()




