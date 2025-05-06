from fastapi import FastAPI
from pydantic import BaseModel
from controllers.tasks import generate_and_upload_video
from controllers.auth import authenticate
from fastapi import Request, HTTPException, Depends
from utils.middleware import get_current_user
app = FastAPI()

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
        await generate_and_upload_video(prompt=prompt.prompt,user=user["userId"])
        print("in here")
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
        response=await authenticate(email=credentials.email, password=credentials.password)
        print("login successful",response)
        return {"message": "Login successful",
                "response":response
                }
    except Exception as e:
        print("something went wrong", e)
        raise HTTPException(status_code=400, detail="Invalid credentials")
