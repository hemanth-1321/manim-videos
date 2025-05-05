from fastapi import FastAPI
from pydantic import BaseModel
from controllers.tasks import generate_and_upload_video
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


class Prompt(BaseModel):
    prompt: str


@app.post("/submit")
async def submit_prompt(prompt: Prompt):
    try:
       await generate_and_upload_video(prompt=prompt)
       print("in here")
    except Exception as e:
        
        print("somthing wet wrong".e)
    return {"received_prompt": prompt.prompt}

