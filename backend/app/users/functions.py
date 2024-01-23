import uuid

import aiofiles
from app.users.models import User
from sqlalchemy.future import select
from fastapi import UploadFile


from app.settings import SETTINGS


async def get_user_by_email(*, session, email: str):
    query = await session.execute(select(User).where(User.email == email))
    return query.scalar_one()


async def get_user_by_id(*, session, id: int):
    query = await session.execute(select(User).where(User.id == id))
    return query.scalar_one()


def get_user_claims(user) -> dict:
    return {"user_id": user["id"], "user_email": user["email"]}


async def save_profile_img(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    await save_file(file=file, file_name=f"{SETTINGS.user_profile_img}/{file_name}")
    return file_name


async def save_file(file, file_name: str):
    async with aiofiles.open(file_name, "wb+") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
