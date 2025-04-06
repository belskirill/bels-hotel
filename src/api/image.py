import shutil

from fastapi import APIRouter, UploadFile

from src.service.image import ImageService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/image", tags=["image"])


@router.post("")
async def uplodad_image(file: UploadFile):
    await ImageService().get_image(file)


