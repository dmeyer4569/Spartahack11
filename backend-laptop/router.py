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

class DeleteItem(BaseModel):
    id: int

    class Config:
        orm_mode = True

@main_router.get("/locations", response_model=List[LocationOut],tags=["Select"])
async def get_locations(db: AsyncSession = Depends(get_db)):

    raw_result = await db.scalars(
        select(Location)
    )
    return raw_result

@main_router.get("/items", response_model=List[PantryOut], tags=["Select"])
async def get_items(db: AsyncSession = Depends(get_db)):
    raw_result = await db.scalars(
        select(Pantry)
    )
    return raw_result

@main_router.delete("/remove/{item_id}", tags=["Delete"])
@main_router.delete("/remove/{item_id}", tags=["Delete"])
async def del_item(item_id: int, db: AsyncSession = Depends(get_db)):

    # get item
    result = await db.execute(
        select(Pantry).where(Pantry.id == item_id)
    )
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    location_id = item.location_id  # temp save

    # rm -r item :p
    await db.delete(item)
    await db.commit()

    # heck if location ahs item, if not deleet
    remaining = await db.execute(
        select(Pantry).where(Pantry.location_id == location_id)
    )
    remaining_items = remaining.scalars().first()

    # location = 0, delete
    if not remaining_items:
        loc_result = await db.execute(
            select(Location).where(Location.id == location_id)
        )
        location = loc_result.scalars().first()
        if location:
            await db.delete(location)
            await db.commit()

    return {"detail": f"Item with id {item_id} deleted successfully"}
