import asyncio
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.models import Hotels

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"]
)

@router.get("/")
@cache(expire=20)
async def get_hotels():
    await asyncio.sleep(3)
    return await HotelDAO.find_all()

@router.get("/{name}")
async def get_hotel_name(name: str = Hotels.name):
    return await HotelDAO.find_all(name=name)

@router.get("/id/{id}")
async def get_hotel_id(id: int = Hotels.id):
    return await HotelDAO.find_all(id=id)