from typing import Optional
from pydantic import BaseModel


class CerateFood(BaseModel):
    name: str
    description: str
    img: str


class ReturnFood(BaseModel):
    id: int
    name: str
    description: str
    img: str


class FoodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    img: Optional[str] = None
