from pydantic import BaseModel, EmailStr, Field


class UserRegisterResponse(BaseModel):
    name: str
    message: str

class UserRegisterRequest(BaseModel):
    name: str
    password: str = Field(min_length=6, max_length=32)
    email: EmailStr


class UserLoginRespons(BaseModel):
    name: str
    message: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str