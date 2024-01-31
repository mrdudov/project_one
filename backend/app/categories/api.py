from typing import List


from fastapi import Depends, APIRouter, HTTPException, Response, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db import get_session
from app.categories.models import Category
from app.categories.schemas import ReturnCategory, CreateCategory, CategoryUpdate


router = APIRouter(prefix="/category", tags=["category"])


@router.get("/categories")
async def get_categories(
    session: AsyncSession = Depends(get_session),
) -> List[ReturnCategory]:
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    return categories


@router.get("/categories/{category_id}")
async def get_category(
    category_id: int,
    session: AsyncSession = Depends(get_session),
) -> ReturnCategory:
    query = await session.execute(select(Category).where(Category.id == category_id))
    return query.scalar_one()


@router.post("/categories")
async def create_category(
    category: CreateCategory,
    session: AsyncSession = Depends(get_session),
) -> ReturnCategory:
    new_category = Category(**category.model_dump())
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    session: AsyncSession = Depends(get_session),
):
    statement = select(Category).where(Category.id == category_id)
    results = await session.execute(statement)
    category = results.scalar_one()
    await session.delete(category)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/categories/{category_id}")
async def patch_category(
    category_id: int,
    category: CategoryUpdate,
    session: AsyncSession = Depends(get_session),
) -> ReturnCategory:
    db_category = await session.get(Category, category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    category_data = category.model_dump(exclude_unset=True)

    for key, value in category_data.items():
        setattr(db_category, key, value)

    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category
