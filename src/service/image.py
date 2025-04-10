import shutil
from fastapi import UploadFile
from src.service.base import BaseService

from src.tasks.tasks import resize_image


class ImageService(BaseService):
    async def get_image(self, file: UploadFile):
        image_path = f"src/static/image/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)
        resize_image.delay(image_path)
