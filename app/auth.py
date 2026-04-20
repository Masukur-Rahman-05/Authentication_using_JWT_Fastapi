import os
from dotenv import load_dotenv
from jose import JWTError,jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta
from typing import Optional

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_pass:str,hashed_pass:str)->bool:
    return pwd_context.verify(plain_pass,hashed_pass)

def create_access_token(data:dict, expire_delta:Optional[timedelta]=None)->str:

    to_encode = data.copy()

    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def decode_token(token:str)-> Optional[str]:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithm=ALGORITHM)
        email : str = payload.get("sub")
        return email
    except JWTError:
        return None
    
    

