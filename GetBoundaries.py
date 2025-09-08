#Select top-left boundary and bottom-right boundary for the area you want
# x, y, w and h are given
# Can be used getting boundary of roll number and each question

from pdf2image import convert_from_path
import cv2
import os

pdf_path = "quiz1/20250901104510_00002.pdf" 
output_folder = "output_images"
os.makedirs(output_folder, exist_ok=True)

pages = convert_from_path(pdf_path, dpi=300)
first_page = pages[0]
img_path = os.path.join(output_folder, "page1.png")
first_page.save(img_path, "PNG")

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
        print(f"Clicked at: x={x}, y={y}")
        if len(coords) == 2:
            cv2.rectangle(img, coords[0], coords[1], (0, 255, 0), 2)
            cv2.imshow("Select Box", img)

            x1_orig = int(coords[0][0] / scale)
            y1_orig = int(coords[0][1] / scale)
            x2_orig = int(coords[1][0] / scale)
            y2_orig = int(coords[1][1] / scale)

            w_orig = x2_orig - x1_orig
            h_orig = y2_orig - y1_orig
            print(f"x, y, w, h = {x1_orig}, {y1_orig}, {w_orig}, {h_orig}")

# Show image and set callback
scale = 0.2 
img_scaled = cv2.resize(img, (0,0), fx=scale, fy=scale)

cv2.imshow("Select Roll Number Box", img_scaled)
cv2.setMouseCallback("Select Roll Number Box", click_event)

print("Click top-left and bottom-right corners of the roll number box.")
cv2.waitKey(0)
cv2.destroyAllWindows()
