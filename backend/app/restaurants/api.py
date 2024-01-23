from typing import List


from fastapi import Depends, APIRouter, HTTPException, Response, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db import get_session
from app.restaurants.models import Restaurant
from app.restaurants.schemas import ReturnRestaurant, CerateRestaurant, RestaurantUpdate
from app.tools.functions import handle_db_exceptions

router = APIRouter(prefix="/restaurant", tags=["restaurant"])


@router.get("/restaurants")
async def get_restaurants(
    session: AsyncSession = Depends(get_session),
) -> List[ReturnRestaurant]:
    result = await session.execute(select(Restaurant))
    restaurants = result.scalars().all()
    return [
        ReturnRestaurant(
            id=restaurant.id,
            name=restaurant.name,
            description=restaurant.description,
            address=restaurant.address,
            longitude=restaurant.longitude,
            latitude=restaurant.latitude,
        )
        for restaurant in restaurants
    ]


@router.get("/restaurants/{restaurant_id}")
async def get_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(get_session),
) -> ReturnRestaurant:
    query = await session.execute(
        select(Restaurant).where(Restaurant.id == restaurant_id)
    )
    restaurant = handle_db_exceptions(query)

    return ReturnRestaurant(
        id=restaurant.id,
        name=restaurant.name,
        description=restaurant.description,
        address=restaurant.address,
        longitude=restaurant.longitude,
        latitude=restaurant.latitude,
    )


@router.post("/restaurants")
async def create_restaurant(
    restaurant: CerateRestaurant,
    session: AsyncSession = Depends(get_session),
) -> ReturnRestaurant:
    new_restaurant = Restaurant(**restaurant.model_dump())
    session.add(new_restaurant)
    await session.commit()
    await session.refresh(new_restaurant)
    return new_restaurant


@router.delete("/restaurants/{restaurant_id}")
async def delete_restaurant(
    restaurant_id: int,
    session: AsyncSession = Depends(get_session),
):
    statement = select(Restaurant).where(Restaurant.id == restaurant_id)
    results = await session.execute(statement)
    restaurant = results.scalar_one()
    await session.delete(restaurant)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/restaurants/{restaurant_id}")
async def patch_restaurant(
    restaurant_id: int,
    restaurant: RestaurantUpdate,
    session: AsyncSession = Depends(get_session),
) -> ReturnRestaurant:
    db_restaurant = await session.get(Restaurant, restaurant_id)
    if not db_restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found",
        )

    restaurant_data = restaurant.model_dump(exclude_unset=True)

    for key, value in restaurant_data.items():
        setattr(db_restaurant, key, value)

    session.add(db_restaurant)
    await session.commit()
    await session.refresh(db_restaurant)
    return db_restaurant
