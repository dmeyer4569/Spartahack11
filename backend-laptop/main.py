from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from session import init_db, get_db
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from router import main_router
from filler_router import filler_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(main_router, prefix="/api") # everything? Not decided as of rn
app.include_router(filler_router, prefix="/testing") # fill the db for testing purposes

