import uuid

import aiofiles
from fastapi import UploadFile

from app.settings import SETTINGS


async def save_file(file, file_name: str):
    async with aiofiles.open(file_name, "wb+") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)


async def save_food_img(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    await save_file(file=file, file_name=f"{SETTINGS.food_img_path}/{file_name}")
    return file_name
