from fastapi import APIRouter
from face_recognition import capture_face, train_model, recognize_face
from models import User

router = APIRouter()

@router.post("/capture/")
async def capture(user: User):
    return await capture_face(user.user_id, user.name)

@router.post("/train/")
async def train():
    return await train_model()

@router.get("/recognize/")
async def recognize():
    return await recognize_face()
@router.get("/attendance/")
async def get_attendance():
    records = await attendance_collection.find().to_list(length=100)
    return records
