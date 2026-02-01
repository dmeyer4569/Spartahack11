from session import get_db
from fastapi import Depends, APIRouter, HTTPException, Path, status, File, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Location, Pantry
from typing import List
from datetime import date
import os

rpi_router = APIRouter()




@rpi_router.post("/rpi_upload", tags=["Select"])
async def new_locations(
    audio_file: UploadFile = File(),
    images: List[UploadFile] = File(),
    db: AsyncSession = Depends(get_db)
    ):
    if audio_file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No Audio File")
    
    upload_audio_dir = "uploads/audio"
    upload_img_dir = "uploads/images"

    os.makedirs(upload_audio_dir, exist_ok=True)
    os.makedirs(upload_img_dir, exist_ok=True)

    for image in images:
        filepath = os.path.join(upload_img_dir, image.filename)

        contents = await image.read()
        with open(filepath, "wb") as f:
            f.write(contents)
        print(f"Image saved {image.filename}")

    filepath_audio = os.path.join(upload_audio_dir, audio_file.filename)

    audio_contents = await audio_file.read()
    with open(filepath_audio, "wb") as f:
        f.write(audio_contents)
    print(f"AudioFile saved {audio_file.filename}")

    return HTTPException(status_code=status.HTTP_200_OK, detail="Successfully uploaded everything")
