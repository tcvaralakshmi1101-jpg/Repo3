import easyocr
import cv2
import matplotlib.pyplot as plt
import os
import time
import csv
import random

# 👉 Use full image path
image_path = r'C:\Users\VARALAKSHMI T C\Desktop\mini project\car.jpg'
db_file = 'vehicle_data.csv'
speed_limit = 80

# 👉 Check if file exists
if not os.path.exists(image_path):
    print("❌ Error: Image file not found. Check the path!")
    exit()

# 👉 Read image
img = cv2.imread(image_path)

# 👉 Check if image loaded properly
if img is None:
    print("❌ Error: Unable to load image!")
    exit()

# 👉 Convert BGR to RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 👉 Initialize EasyOCR
reader = easyocr.Reader(['en'])

# 👉 Detect text
results = reader.readtext(img_rgb)

plate_text = "UNKNOWN"

# 👉 Draw bounding boxes and print results
for (bbox, text, prob) in results:
    print(f"Detected: {text} (Confidence: {prob:.2f})")

    if len(text) >= 5:
        plate_text = text

    (top_left, top_right, bottom_right, bottom_left) = bbox

    top_left = tuple(map(int, top_left))
    bottom_right = tuple(map(int, bottom_right))

    # Draw rectangle
    cv2.rectangle(img_rgb, top_left, bottom_right, (0, 255, 0), 2)

    # Put detected text
    cv2.putText(img_rgb, text, top_left,
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

# -----------------------------
# 🛣️ LANE DETECTION (VISIBLE)
# -----------------------------
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150)

cv2.imshow("Lane Detection (Simulated)", edges)

# -----------------------------
# ⚡ SPEED ESTIMATION
# -----------------------------
speed = random.randint(40, 120)

# -----------------------------
# 💳 BILLING SYSTEM
# -----------------------------
if speed > speed_limit:
    fine = (speed - speed_limit) * 10
    status = "Overspeeding"
else:
    fine = 0
    status = "Within Limit"

# -----------------------------
# 💾 DATABASE STORAGE (CSV)
# -----------------------------
file_exists = os.path.isfile(db_file)

with open(db_file, mode='a', newline='') as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["Plate", "Speed", "Fine", "Status", "Time"])

    writer.writerow([plate_text, speed, fine, status, time.ctime()])

# -----------------------------
# 📊 LIVE DASHBOARD (TERMINAL)
# -----------------------------
print("\n==============================")
print("📊 LIVE SYSTEM DASHBOARD")
print("==============================")
print(f"🚗 Plate Number : {plate_text}")
print(f"⚡ Speed        : {speed} km/h")
print(f"📌 Status       : {status}")
print(f"💳 Fine         : ₹{fine}")
print("==============================\n")

# 👉 Show image
plt.imshow(img_rgb)
plt.axis('off')
plt.title("Detected License Plate Text")
plt.show()

# Keep lane window open
cv2.waitKey(0)
cv2.destroyAllWindows()