import uuid

import aiofiles
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from fastapi import HTTPException, UploadFile

from app.settings import SETTINGS


def handle_db_exceptions(query):
    try:
        return query.scalar_one()
    except NoResultFound as exc:
        raise HTTPException(status_code=404, detail=f"item not found. {exc}.")
    except MultipleResultsFound as exc:
        HTTPException(status_code=404, detail=f"multiple items found. {exc}.")


async def save_file(file, file_name: str):
    async with aiofiles.open(file_name, "wb+") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)


async def save_food_img(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    await save_file(file=file, file_name=f"{SETTINGS.food_img_path}/{file_name}")
    return file_name
