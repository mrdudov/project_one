from typing import List
from sqlmodel import Relationship, SQLModel, Field

from app.foods.models import Food


class OrderFoodLink(SQLModel, table=True):
    order_id: int = Field(
        default=None,
        foreign_key="order.id",
        primary_key=True,
    )
    food_id: int = Field(
        default=None,
        foreign_key="food.id",
        primary_key=True,
    )


class Order(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    status: str = Field(default="")

    foods: List[Food] = Relationship(
        back_populates="order",
        link_model=OrderFoodLink,
    )
