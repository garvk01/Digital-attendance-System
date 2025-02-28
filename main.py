from fastapi import FastAPI,Request
from routes import router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

app = FastAPI(title="Face Recognition API")

app.include_router(router)

@app.get("/")
async def home():
    return {"message": "Face Recognition API is running!"}
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="index.html")
# app.mount("/static", StaticFiles(directory="static"), name="static")
conn = MongoClient("mongodb+srv://kapoorgarv03:<garv9876>@dasp.3brxy.mongodb.net/")
