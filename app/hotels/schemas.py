from pydantic import BaseModel, ConfigDict, Json

class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: Json
    room_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)