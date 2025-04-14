import shutil

from fastapi import APIRouter, UploadFile, HTTPException

from src.service.image import ImageService


router = APIRouter(prefix="/image", tags=["image"])


@router.post("")
async def uplodad_image(file: UploadFile):
    if file.content_type in ["image/png", "image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Недопустимый тип файла")
    await ImageService().get_image(file)


