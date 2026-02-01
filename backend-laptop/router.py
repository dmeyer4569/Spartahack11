from session import get_db
from typing import List
from fastapi import Depends, APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Location, Pantry
from datetime import date

main_router = APIRouter()

class LocationOut(BaseModel):
    id: int
    location: str

    class Config:
        orm_mode = True

class PantryOut(BaseModel):
    id: int
    name: str
    expire: date
    quantity: int
    img_path: str
    location_id: int

    class Config:
        orm_mode = True

@main_router.get("/locations", tags=["Select"])
async def get_locations(db: AsyncSession = Depends(get_db)):

    raw_result = await db.scalars(
        select(Location)
    )
    location_data = [{"id": row.id, "location": row.location} for row in raw_result]

    return location_data

@main_router.get("/items", response_model=List[PantryOut], tags=["Select"])
async def get_items(db: AsyncSession = Depends(get_db)):
    raw_result = await db.scalars(
        select(Pantry)
    )
    return raw_result
