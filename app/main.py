from contextlib import asynccontextmanager
import time
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI, version

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router import router as router_users
from app.logger import logger

from prometheus_fastapi_instrumentator import Instrumentator


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)

# @app.get("/hotels/{hotel_id}")
# def get_hotels(hotel_id: int, date_from, date_to):
#     return hotel_id, date_from, date_to

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response

# import uvicorn
# if __name__ =="__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# origins = ["http://localhost:3000"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_cridentials=True,
#     allow_methods = ["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
#     allow_headers = ["COntent-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin", "Access-Autorization"],

# )


app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')

@app.on_event("startup")
def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admmin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

app.mount("/static", StaticFiles(directory="app/static"), "static")

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)