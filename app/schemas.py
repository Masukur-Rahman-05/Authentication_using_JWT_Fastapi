from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr 
    username : str = Field(min_length = 5, max_length=50)
    password : str = Field(min_length=6)

    class Config:
        json_schemas_extra = {
            "example":{
                "email":"example@email.com",
                "username":"username123",
                "password":"mypassword456"
            }
        }


class UserOut(BaseModel):
    id : int
    email: EmailStr 
    username : str 

    class Config:
        from_attributes = True
        json_schemas_extra = {
            "example":{
                "email":"alice@email.com",
                "username":"alice",
            }
        }

class Token(BaseModel):
    access_token : str
    token_type : str = "bearer"

    class Config:
        json_schemas_extra = {
            "example":{
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class Token_data(BaseModel):
    email : Optional[EmailStr] = None
            