from fastapi import FastAPI, UploadFile, File, HTTPException
import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials, firestore
from pyzbar.pyzbar import decode
import io
import threading
from fastapi.responses import StreamingResponse

# Initialize Firebase
cred = credentials.Certificate("path/to/firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

# Face recognition model (dummy example, replace with actual model)
def recognize_face(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces) > 0

# # QR Code Scanner
# def scan_qr_code(image_bytes):
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     decoded_objects = decode(img)
#     if decoded_objects:
#         return decoded_objects[0].data.decode('utf-8')  # Returning the first detected QR code
#     return None

@app.post("/mark_attendance/face")
async def mark_attendance_face(image: UploadFile = File(...)):
    image_bytes = await image.read()
    if recognize_face(image_bytes):
        doc_ref = db.collection("attendance").add({"type": "face", "status": "present"})
        return {"message": "Attendance marked successfully via Face Recognition"}
    else:
        raise HTTPException(status_code=400, detail="Face not recognized")

@app.post("/mark_attendance/qr")
async def mark_attendance_qr(image: UploadFile = File(...)):
    image_bytes = await image.read()
    student_id = scan_qr_code(image_bytes)
    if student_id:
        db.collection("attendance").add({"type": "QR", "student_id": student_id, "status": "present"})
        return {"message": f"Attendance marked for Student ID: {student_id}"}
    else:
        raise HTTPException(status_code=400, detail="Invalid QR Code")

@app.get("/attendance")
async def get_attendance():
    docs = db.collection("attendance").stream()
    attendance_data = [{doc.id: doc.to_dict()} for doc in docs]
    return {"attendance_records": attendance_data}

# Live Video Streaming


# Run with: uvicorn main:app --reload