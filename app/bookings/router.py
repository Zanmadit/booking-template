from datetime import date
from fastapi import APIRouter, Depends, Request

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.bookings.models import Bookings
from app.exceptions import RoomCanNotBeBoocked, RoomCanNotBeDeleted
from app.tasks.tasks import send_bookings_confirmation_email
from fastapi_versioning import version


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)): #-> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
@version(2)
async def add_booking(
    room_id: int,  date_from: date, date_to: date,
    user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBoocked
    
    booking_dict = SBooking.model_validate(booking)

    send_bookings_confirmation_email.delay(booking_dict.model_dump(), user.email)
    return booking_dict
    
@router.delete("/{booking_id}")
@version(1)
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.delete(user.id, booking_id)
    if not booking:
        raise RoomCanNotBeDeleted