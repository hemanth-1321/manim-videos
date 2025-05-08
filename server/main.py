from fastapi import FastAPI, Request, HTTPException, Depends
from pydantic import BaseModel
from utils.db import db
from controllers.videoGen import generate_and_upload_video, get_all_videos, get_Users_videos
from controllers.auth import authenticate
from fastapi.middleware.cors import CORSMiddleware
from utils.middleware import get_current_user

app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect()
    print("Prisma connected")

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    print("Prisma disconnected")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Prompt(BaseModel):
    prompt: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/submit")
async def submit_prompt(prompt: Prompt, user=Depends(get_current_user)):
    try:
        await generate_and_upload_video(prompt=prompt.prompt, user=user["userId"])
        print("in her1")
    except Exception as e:
        print("something went wrong", e)
        raise HTTPException(status_code=500, detail="Video generation failed")
    return {
        "received_prompt": prompt.prompt,
        "submitted_by": user["sub"]
    }

@app.post("/login")
async def login(credentials: LoginRequest):
    try:
        response = await authenticate(email=credentials.email, password=credentials.password)
        print("login successful", response)
        return {
            "message": "Login successful",
            "response": response
        }
    except Exception as e:
        print("something went wrong", e)
        raise HTTPException(status_code=400, detail="Invalid credentials")

@app.get("/video")
async def GetVideos():
    try:
        response = await get_all_videos()
        return {"message": "videos", "response": response}
    except Exception as e:
        print("something went wrong", e)
        raise HTTPException(status_code=500, detail="Failed to fetch videos")

@app.get("/user/video")
async def GetUserVideos(user=Depends(get_current_user)):
    try:
        response = await get_Users_videos(user=user)
        return {"message": "videos", "response": response}
    except Exception as e:
        print("something went wrong", e)
        raise HTTPException(status_code=500, detail="Failed to fetch videos")
