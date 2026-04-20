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
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))

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

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db:Session = Depends(get_db)
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
    if not user:
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

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login",response_model=Token)
def login(
    form_data : OAuth2PasswordRequestForm = Depends(),
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
            headers={"WWW-Authenticate":"Bearer"}
        )
    
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub":user.email},
        expire_delta=access_token_expire
    )

    return {"access_token":access_token,"token_type":"bearer"}


@app.get("/profile",response_model=UserOut)
def get_user(current_user: User = Depends(get_current_user)):
    return current_user



@app.get("/users",response_model=list[UserOut])
def get_users(
    current_user:User = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    users = db.query(User).all()
    return users

