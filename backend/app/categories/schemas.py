from typing import Optional
from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    description: str


class ReturnCategory(BaseModel):
    id: int
    name: str
    description: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
