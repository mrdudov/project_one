from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.users.models import User
from app.users.schemas import ReturnUser
from app.users.functions import get_user_by_id


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)) -> List[ReturnUser]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [
        ReturnUser(id=user.id, email=user.email, profile_img=user.profile_img)
        for user in users
    ]


@router.get("/user")
async def get_users(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> ReturnUser:
    user = await get_user_by_id(session=session, id=user_id)

    return ReturnUser(id=user.id, email=user.email, profile_img=user.profile_img)
