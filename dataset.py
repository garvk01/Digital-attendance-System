import cv2
import os
import sqlite3
dataset_path = "dataset"
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)
conn = sqlite3.connect("face_database.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, 
        name TEXT
    )
""")
conn.commit()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

user_id = input("Enter User ID (Number): ")
user_name = input("Enter Name: ")

c.execute("INSERT INTO users (id, name) VALUES (?, ?)", (user_id, user_name))
conn.commit()

count = 0
while count < 40:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = gray[y:y + h, x:x + w]
        img_name = f"{dataset_path}/{user_id}_{count}.jpg"
        cv2.imwrite(img_name, face)

        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f"Captured {count}/40", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Face Capture", frame)

    if cv2.waitKey(1) == 27 or count >= 50:
        break

cap.release()
cv2.destroyAllWindows()
conn.close()

print(f"✅ {count} images saved in '{dataset_path}' for User ID: {user_id}")
print(f"✅ User data saved in database: ID = {user_id}, Name = {user_name}")
