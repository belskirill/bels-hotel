from typing import Annotated

from pydantic import BaseModel, Field
from fastapi import Depends

class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int

class Rooms(RoomsAdd):
    id: int


class RoomsPath(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


