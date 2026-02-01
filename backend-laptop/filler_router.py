from session import get_db
from fastapi import Depends, APIRouter, HTTPException, Path, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Location, Pantry
from datetime import date

filler_router = APIRouter()

class InsertLocation(BaseModel):
    location: str

class InsertItem(BaseModel):
    name: str
    expiration_date: date
    quantity: int
    img_path: str
    location: int



@filler_router.post("/add_location", tags=["Select"])
async def new_locations(location: InsertLocation, db: AsyncSession = Depends(get_db)):

    raw_result_verify = await db.execute(
        select(Location)
        .where(Location.location == location.location)
    )
    location_in_db = raw_result_verify.scalar_one_or_none()

    if location_in_db is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Location exists already")

    new_location = Location(
        location=location.location
    )
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    
    location_dict = jsonable_encoder(new_location)
    
    return {
            "message": "Successfully Inserted!", 
            "location": location.location
    }

@filler_router.post("/add_item", tags=["Select"])
async def new_item(item: InsertItem, db: AsyncSession = Depends(get_db)):


    raw_location_result = await db.execute(
        select(Location)
        .where(Location.id == item.location)
    )
    location_in_db = raw_location_result.scalar_one_or_none()

    if location_in_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    new_item = Pantry(
        name=item.name,
        expire=item.expiration_date,
        quantity=item.quantity,
        img_path=item.img_path,
        location=location_in_db
    )

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)



    return {
        "message": "Successfully Inserted Item!",
        "item": item.name
    }
