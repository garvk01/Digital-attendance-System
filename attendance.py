import cv2
import sqlite3
import csv
import time
import os
import numpy as np
from datetime import datetime

# Load trained model
fname = "recognizer/trainingData.yml"
if not cv2.os.path.isfile(fname):
    print("⚠️ Error: Training data not found! Please train the model first.")
    exit(0)

# Load Haarcascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(fname)

# Connect to SQLite database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Track time
start_time = time.time()
face_detected = False
user_id = None
user_name = None

# CSV file for attendance
csv_filename = "attendance.csv"
today_date = datetime.now().strftime("%Y-%m-%d")

# Read existing attendance records
attendance_records = set()
if os.path.exists(csv_filename):
    with open(csv_filename, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3:
                attendance_records.add((row[0], row[2].split()[0]))  # (User ID, Date)

while True:
    ret, img = cap.read()
    if not ret:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        face_detected = True
        face_roi = gray[y:y + h, x:x + w]

        # Predict user ID and confidence
        user_id, confidence = recognizer.predict(face_roi)
        print(f"Detected ID: {user_id}, Confidence: {confidence}")

        if confidence < 70:
            c.execute("SELECT name FROM users1 WHERE id = ?;", (user_id,))
            result = c.fetchone()
            user_name = result[0] if result else "Unknown"
        else:
            user_name = "Unknown"

        # Draw bounding box and name
        color = (0, 255, 0) if user_name != "Unknown" else (0, 0, 255)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, user_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Face Recognition", img)

    if time.time() - start_time > 5:
        break

    if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()

# If a recognized face is detected, mark attendance
if face_detected and user_name != "Unknown":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if attendance is already marked for today
    if (str(user_id), today_date) in attendance_records:
        print(f"⚠️ Attendance already marked for {user_name} today.")
    else:
        # Write to CSV
        file_exists = os.path.exists(csv_filename)
        with open(csv_filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["User ID", "Name", "Timestamp"])  # Write headers only if file is new
            writer.writerow([user_id, user_name, now])

        print(f"✅ Attendance marked for {user_name} at {now}")
else:
    print("⚠️ No recognized face detected. Attendance not marked.")
