from typing import List


from fastapi import Depends, APIRouter, HTTPException, Response, UploadFile, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db import get_session
from app.foods.models import Food
from app.foods.schemas import ReturnFood, CerateFood, FoodUpdate
from app.tools.functions import save_food_img

router = APIRouter(prefix="/food", tags=["food"])


@router.get("/foods")
async def get_foods(
    session: AsyncSession = Depends(get_session),
) -> List[ReturnFood]:
    result = await session.execute(select(Food))
    foods = result.scalars().all()
    return foods


@router.get("/foods/{food_id}")
async def get_food(
    food_id: int,
    session: AsyncSession = Depends(get_session),
) -> ReturnFood:
    query = await session.execute(select(Food).where(Food.id == food_id))

    return query.scalar_one()


@router.post("/foods")
async def create_food(
    food: CerateFood,
    session: AsyncSession = Depends(get_session),
) -> ReturnFood:
    new_food = Food(**food.model_dump())
    session.add(new_food)
    await session.commit()
    await session.refresh(new_food)
    return new_food


@router.delete("/foods/{food_id}")
async def delete_food(
    food_id: int,
    session: AsyncSession = Depends(get_session),
):
    statement = select(Food).where(Food.id == food_id)
    results = await session.execute(statement)
    food = results.scalar_one()
    await session.delete(food)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/foods/{food_id}")
async def patch_food(
    food_id: int,
    food: FoodUpdate,
    session: AsyncSession = Depends(get_session),
) -> ReturnFood:
    db_food = await session.get(Food, food_id)
    if not db_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found",
        )

    food_data = food.model_dump(exclude_unset=True)

    for key, value in food_data.items():
        setattr(db_food, key, value)

    session.add(db_food)
    await session.commit()
    await session.refresh(db_food)
    return db_food


@router.post("/food-img")
async def set_food_img(
    food_id: int,
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
):
    db_food = await session.get(Food, food_id)
    if not db_food:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Food not found",
        )
    file_name = await save_food_img(file)
    db_food.img = file_name
    session.add(db_food)
    await session.commit()
    await session.refresh(db_food)
    return db_food
