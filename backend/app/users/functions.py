import uuid

from fastapi import UploadFile

from app.settings import SETTINGS
from app.tools.functions import save_file


async def save_user_profile_img(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = f"{SETTINGS.user_profile_img_path}/{file_name}"
    await save_file(file=file, file_name=file_path)
    return file_path
