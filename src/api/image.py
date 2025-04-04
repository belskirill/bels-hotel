import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/image", tags=["image"])


@router.post("")
async def uplodad_image(file: UploadFile, text: str):
    image_path = f"src/static/image/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
    resize_image.delay(image_path)


@router.post("/telegram")
async def telegram_message(text: str):
    return {
        "status": "ok",
        "wallet": text,
    }
