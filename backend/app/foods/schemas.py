from pydantic import BaseModel


class CerateFood(BaseModel):
    name: str
    description: str
    img: str


class ReturnFood(BaseModel):
    id: int
    name: str
    description: str
    img: str
