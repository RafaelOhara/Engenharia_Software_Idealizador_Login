from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv("config.env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data:dict):
    encode= data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp":expire})
    encoded = jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded

def verify_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="TOKEN INVALIDO OU EXPIRADO",

            headers={"WWW-Autheticate":"Bearer"},)
