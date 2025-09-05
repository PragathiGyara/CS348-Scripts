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
clone = img.copy()
coords = []

# Mouse callback function
def click_event(event, x, y, flags, param):
    global coords, img
    if event == cv2.EVENT_LBUTTONDOWN:
        coords.append((x, y))
        print(f"Clicked at: x={x}, y={y}")
        if len(coords) == 2:
            cv2.rectangle(img, coords[0], coords[1], (0, 255, 0), 2)
            cv2.imshow("Select Roll Number Box", img)

            x1, y1 = coords[0]
            x2, y2 = coords[1]
            w = x2 - x1
            h = y2 - y1
            print(f"\nUse these in your OCR script:")
            print(f"x, y, w, h = {x1}, {y1}, {w}, {h}")

# Show image and set callback
scale = 1
img_scaled = cv2.resize(img, (0,0), fx=scale, fy=scale)
cv2.imshow("Select Roll Number Box", img_scaled)
cv2.imshow("Select Roll Number Box", img)
cv2.setMouseCallback("Select Roll Number Box", click_event)

print("Click top-left and bottom-right corners of the roll number box.")
cv2.waitKey(0)
cv2.destroyAllWindows()
