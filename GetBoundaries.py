#Select top-left boundary and bottom-right boundary for the area you want
# x, y, w and h are given
# Can be used getting boundary of roll number and each question

from pdf2image import convert_from_path
import cv2
import os


pdf_path = input("Enter the path to any answer sheet (pdf): ").strip()
page_number = int(input("Enter the page number you want to extract from(starting from 1): ").strip())
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)


pages = convert_from_path(pdf_path, dpi=300)

if page_number < 1 or page_number > len(pages):
    print(f"Invalid page number. This PDF has {len(pages)} pages.")
    exit()

selected_page = pages[page_number - 1]
img_path = os.path.join(output_folder, f"page_{page_number}.png")
selected_page.save(img_path, "PNG")

# Load image with OpenCV
img = cv2.imread(img_path)

total_height, total_width, c = img.shape  

print(f"Image dimensions  Width: {total_width}px, Height: {total_height}px")
coords = []

# Mouse callback function
def click_event(event, x, y, flags, param):
    global coords, img
    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append((x, y))
        # print(f"Clicked at: x={x}, y={y}")
        if len(coords) == 2:
            # cv2.rectangle(img, coords[0], coords[1], (0, 255, 0), 2)
            # cv2.imshow("Select Box", img)
            cv2.rectangle(img_scaled, coords[0], coords[1], (0, 255, 0), 2)
            cv2.imshow("Select Box", img_scaled)

            x1_orig = int(coords[0][0] / scale)
            y1_orig = int(coords[0][1] / scale)
            x2_orig = int(coords[1][0] / scale)
            y2_orig = int(coords[1][1] / scale)

            w_orig = x2_orig - x1_orig
            h_orig = y2_orig - y1_orig
            print(f'{{"x": {x1_orig}, "y": {y1_orig}, "w": {w_orig}, "h": {h_orig}}}')


# Show image and set callback
scale = 0.2 
img_scaled = cv2.resize(img, (0,0), fx=scale, fy=scale)

cv2.imshow("Select Roll Number Box or Answer Box", img_scaled)
cv2.setMouseCallback("Select Roll Number Box or Answer Box", click_event)

print("Click top-left and bottom-right corners of the area you want")
cv2.waitKey(0)
cv2.destroyAllWindows()
