from session import get_db
from fastapi import Depends, APIRouter, HTTPException, Path, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Location, Pantry

main_router = APIRouter()

@main_router.get("/locations", tags=["Select"])
async def get_locations(db: AsyncSession = Depends(get_db)):

    raw_result = await db.execute(
        select(Location)
    )
    location_data = [", ".join(str(v) for v in row._mapping.values()) for row in raw_result]

    return location_data
