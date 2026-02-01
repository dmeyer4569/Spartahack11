from session import get_db
from fastapi import Depends, APIRouter, HTTPException, Path, status, File, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Location, Pantry
from typing import List
from datetime import datetime, date
import os
from stt import stt
from gemini_api import gemini_talk_with_me
import json

rpi_router = APIRouter()


class InsertItem(BaseModel):
    name: str
    expiration_date: date
    quantity: int
    img_path: str
    location: int

# Pure chaos... Even I'm lost :p

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

    img_order = []

    for image in images:
        filepath = os.path.join(upload_img_dir, image.filename)

        contents = await image.read()
        with open(filepath, "wb") as f:
            f.write(contents)

        print(f"Image saved {image.filename}")

        try:
            rank = int(image.filename.split("_", 1)[1].split(".")[0])
        except (IndexError, ValueError):
            print(f"Skipping {image.filename}, bad format")
            continue

        inserted = False
        for i, existing in enumerate(img_order):
            existing_rank = int(existing.split("_", 1)[1].split(".")[0])
            if rank < existing_rank:
                img_order.insert(i, image.filename)
                inserted = True
                break

        if not inserted:
            img_order.append(image.filename)
    print(img_order)


    filepath_audio = os.path.join(upload_audio_dir, audio_file.filename)

    audio_contents = await audio_file.read()
    with open(filepath_audio, "wb") as f:
        f.write(audio_contents)
    print(f"AudioFile saved {audio_file.filename}")

    result = stt(filepath_audio)
    print(f"{result=}")
    gemini_ans = gemini_talk_with_me(result)

    json_result = json.loads(gemini_ans)
    print(f"{gemini_ans=}")

    img_tracker = 0
    print(f"{json_result=}")
    for item in json_result:
        raw_location_result = await db.execute(
            select(Location)
            .where(Location.location == item["location"])
        )

        location_in_db = raw_location_result.scalar_one_or_none()

        if location_in_db is None:
            new_location = Location(
            location=item["location"]
            )
            db.add(new_location)
            await db.commit()
            await db.refresh(new_location)
            location_in_db = new_location

        item_image = img_order[img_tracker]
        filepath = item_image

        print(f"the item image we are committing are {filepath=}")
        item_expiry = datetime.strptime(item["expires"], "%Y-%m-%d").date()

        new_item = Pantry(
            name=item["item"],
            expire=item_expiry,
            quantity=item["quantity"],
            img_path=filepath,
            location=location_in_db
        )
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)
        img_tracker+=1

    return HTTPException(status_code=status.HTTP_200_OK, detail="Successfully uploaded everything"), json_result

