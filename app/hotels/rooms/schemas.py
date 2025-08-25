from pydantic import BaseModel, ConfigDict, Json

class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: Json
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)