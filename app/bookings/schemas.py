from datetime import date
from pydantic import BaseModel, ConfigDict

# есть билиотека SQLModel

class SBooking(BaseModel):    # S - means Schema
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    # UserWarning: Valid config keys have changed in V2: * 'orm_mode' has been renamed to 'from_attributes'
#   warnings.warn(message, UserWarning)


    model_config = ConfigDict(from_attributes=True)