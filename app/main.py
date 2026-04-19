import os
from dotenv import load_dotenv
from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security  import HTTPBearer,HTTPAuthorizationCredentials,OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import User
from .schemas import UserCreate,UserOut,Token,Token_data
from .auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_token
)

load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI Lab 4"),
    description="JWT Authentication with FastAPI and PostgreSQL",
    version="1.0.0"
)


security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db:Session = Depends(SessionLocal)
) -> User :
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate":"Bearer"}
    )

    token = credentials.credentials

    email = decode_token(token)
    if email is None:
        raise credentials_exception
    

    user = db.query(User).filter(User.email == email).first()
    if not User:
        raise credentials_exception
    
    return user

@app.post("/signup",response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(payload:UserCreate,db:Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        (User.email == payload.email) | (User.username == payload.username)
    ).first()

    if existing_user:
        if existing_user.email == payload.email:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Email already exists"
            )
        else:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Username already exists"
            )
        
    hashed_password = hash_password(payload.password)

    new_user = User(
        email = payload.email,
        username = payload.username,
        password = hashed_password
    )
