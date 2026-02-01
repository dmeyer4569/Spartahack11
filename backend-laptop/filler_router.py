from session import get_db
from fastapi import Depends, APIRouter, HTTPException, Path, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Location, Pantry

filler_router = APIRouter()

class InsertLocation(BaseModel):
    location: str

@filler_router.post("/add_location", tags=["Select"])
async def get_locations(location: InsertLocation, db: AsyncSession = Depends(get_db)):

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
