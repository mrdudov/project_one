from decimal import Decimal

from sqlmodel import SQLModel, Field


class Food(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field()
    price: Decimal
    description: str = Field()
    img: str = Field(default="")
