from sqlmodel import SQLModel, Field


class Restaurant(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str = Field(default="")
    address: str = Field(default="")
    longitude: float = Field(default=0.0)
    latitude: float = Field(default=0.0)
