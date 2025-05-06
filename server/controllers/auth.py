from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from passlib.hash import bcrypt
from jose import jwt
from prisma import Prisma
from datetime import datetime, timedelta
import os

app = FastAPI()
db = Prisma()

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate(email: str, password: str):
    await db.connect()
    user = await db.user.find_unique(where={"email": email})

    if user:
        if not bcrypt.verify(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        hashed_password = bcrypt.hash(password)
        user = await db.user.create(data={
            "email": email,
            "password": hashed_password
        })
    await db.disconnect()

    token = create_access_token(data={"sub": email,"userId": user.id})
    return  token 



