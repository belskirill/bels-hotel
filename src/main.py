from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.init import redis_manager  # noqa: E402

from src.api.auth import router as router_auth  # noqa: E402
from src.api.hotels import router as router_hotels  # noqa: E402
from src.api.rooms import router as router_rooms  # noqa: E402
from src.api.bookings import router as router_bookings  # noqa: E402
from src.api.facilities import router as router_facilities  # noqa: E402
from src.api.image import router as router_images  # noqa: E402


from fastapi_cache import FastAPICache  # noqa: E402
from fastapi_cache.backends.redis import RedisBackend  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()

    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(title="BELS docs", lifespan=lifespan)


app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
