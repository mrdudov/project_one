from typing import List

from fastapi import Depends, APIRouter, HTTPException, Response, status, UploadFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.users.models import User
from app.users.schemas import ReturnUser, CreateUser, UpdateUser
from app.users.functions import save_user_profile_img


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/users")
async def get_users(
    session: AsyncSession = Depends(get_session),
) -> List[ReturnUser]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> ReturnUser:
    query = await session.execute(select(User).where(User.id == user_id))
    return query.scalar_one()


@router.post("/users")
async def create_user(
    user: CreateUser,
    session: AsyncSession = Depends(get_session),
) -> ReturnUser:
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    statement = select(User).where(User.id == user_id)
    results = await session.execute(statement)
    user = results.scalar_one()
    await session.delete(user)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/users/{user_id}")
async def patch_user(
    user_id: int,
    user: UpdateUser,
    session: AsyncSession = Depends(get_session),
) -> ReturnUser:
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user_data = user.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.post("/user-img")
async def set_user_img(
    user_id: int,
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    file_name = await save_user_profile_img(file)
    db_user.profile_img = file_name
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
