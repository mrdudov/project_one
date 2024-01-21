from decimal import Decimal

from typing import Optional
from pydantic import BaseModel


class CerateFood(BaseModel):
    name: str
    price: Decimal
    description: str
    img: str


class ReturnFood(BaseModel):
    id: int
    name: str
    price: Decimal
    description: str
    img: str


class FoodUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    description: Optional[str] = None
    img: Optional[str] = None
