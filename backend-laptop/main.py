import uvicorn
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from session import init_db, get_db
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from router import main_router
from filler_router import filler_router
from rpi_router import rpi_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://10.249.231.63:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads/images", StaticFiles(directory="uploads/images"), name="images")

app.include_router(main_router, prefix="/api") # everything? Not decided as of rn
app.include_router(filler_router, prefix="/testing") # fill the db for testing purposes
app.include_router(rpi_router, prefix="/rpi") # anything rpi related 


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)