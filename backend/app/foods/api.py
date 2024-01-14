from typing import List


from fastapi import Depends, APIRouter, HTTPException, UploadFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


from app.db import get_session
from app.foods.models import Food
from app.foods.schemas import ReturnFood, CerateFood

router = APIRouter(prefix="/food", tags=["food"])


def handle_db_exceptions(query):
    try:
        return query.scalar_one()
    except NoResultFound as exc:
        raise HTTPException(status_code=404, detail=f"item not found. {exc}.")
    except MultipleResultsFound as exc:
        HTTPException(status_code=404, detail=f"multiple items found. {exc}.")


@router.get("/foods")
async def get_foods(session: AsyncSession = Depends(get_session)) -> List[ReturnFood]:
    result = await session.execute(select(Food))
    foods = result.scalars().all()
    return [
        ReturnFood(
            id=food.id, name=food.name, description=food.description, img=food.img
        )
        for food in foods
    ]


@router.get("/food")
async def get_food(
    food_id: int, session: AsyncSession = Depends(get_session)
) -> ReturnFood:
    query = await session.execute(select(Food).where(Food.id == food_id))
    food = handle_db_exceptions(query)

    return ReturnFood(
        id=food.id, name=food.name, description=food.description, img=food.img
    )
