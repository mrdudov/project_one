from typing import Optional
from pydantic import BaseModel


class CerateRestaurant(BaseModel):
    name: str
    description: str
    address: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None

class ReturnRestaurant(BaseModel):
    id: int
    name: str
    description: str
    address: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
