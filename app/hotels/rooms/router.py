from app.hotels.router import router
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.models import Hotels


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int = Hotels.id):
    return await RoomsDAO.find_by_id(hotel_id)