from sqlmodel import SQLModel, Field, AutoString
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, sa_type=AutoString)
    profile_img: str = Field(default="")
    password: str = Field()
