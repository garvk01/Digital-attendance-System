import cv2
import os
import numpy as np
import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users1 (id INTEGER PRIMARY KEY, name TEXT)''')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
user_id = input("Enter User ID (Number): ")
user_name = input("Enter User Name: ")
c.execute("INSERT INTO users1 (id, name) VALUES (?, ?)", (user_id, user_name))
conn.commit()
dataset_dir = "dataset"
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)
cap = cv2.VideoCapture(0)
count = 0
while count < 50:
    ret, frame = cap.read()
    if not ret:
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=8, minSize=(70, 70))
    for (x, y, w, h) in faces:
        count += 1
        face_roi = gray[y:y+h, x:x+w]
        face_roi = cv2.equalizeHist(face_roi)
        face_roi = cv2.resize(face_roi, (200, 200))
        filename = f"{dataset_dir}/{user_id}_{count}.jpg"
        cv2.imwrite(filename, face_roi)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("Capturing Faces", frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
print(f"✅ {count} high-quality face images saved for User ID {user_id}")
def train_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, ids = [], []
    image_paths = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.endswith(".jpg")]
    for image_path in image_paths:
        img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        face_id = int(os.path.basename(image_path).split("_")[0])
        faces.append(img_gray)
        ids.append(face_id)
    print("🔄 Training model, please wait...")
    recognizer.train(faces, np.array(ids))
    recognizer.save("recognizer/trainingData.yml")
    print("✅ Model trained and saved as 'trainingData.yml'")
train_model()



