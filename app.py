import streamlit as st
import easyocr
import cv2
import numpy as np
import tempfile
import random
import csv
import time
import os

st.title("🚗 Automatic License Plate Recognition System")

# Upload image
uploaded_file = st.file_uploader("Upload Vehicle Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    img = cv2.imread(tfile.name)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # OCR
    reader = easyocr.Reader(['en'])
    results = reader.readtext(img_rgb)

    plate_text = "UNKNOWN"

    for (bbox, text, prob) in results:
        if len(text) >= 5:
            plate_text = text

        (top_left, _, bottom_right, _) = bbox
        top_left = tuple(map(int, top_left))
        bottom_right = tuple(map(int, bottom_right))

        cv2.rectangle(img_rgb, top_left, bottom_right, (0,255,0), 2)
        cv2.putText(img_rgb, text, top_left,
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0,255,0), 2)

    # Simulated features
    speed = random.randint(40, 120)
    speed_limit = 80

    if speed > speed_limit:
        fine = (speed - speed_limit) * 10
        status = "Overspeeding"
    else:
        fine = 0
        status = "Within Limit"

    # Display image
    st.image(img_rgb, caption="Detected License Plate", use_column_width=True)

    # Dashboard
    st.subheader("📊 Vehicle Details")
    st.write(f"🚗 Plate Number: {plate_text}")
    st.write(f"⚡ Speed: {speed} km/h")
    st.write(f"📌 Status: {status}")
    st.write(f"💳 Fine: ₹{fine}")

    # Save to CSV
    db_file = "vehicle_data.csv"
    file_exists = os.path.isfile(db_file)

    with open(db_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Plate", "Speed", "Fine", "Status", "Time"])
        writer.writerow([plate_text, speed, fine, status, time.ctime()])

    st.success("💾 Data stored successfully!")