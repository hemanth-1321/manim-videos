from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()  

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_user(request: Request):
    authorization = request.headers.get("Authorization")
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format. Expected: Bearer <token>")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
