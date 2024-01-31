from typing import Optional
from pydantic import EmailStr, BaseModel


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    profile_img: str


class ReturnUser(BaseModel):
    id: int
    email: EmailStr
    profile_img: str


class UpdateUser(BaseModel):
    email: Optional[EmailStr] = None
