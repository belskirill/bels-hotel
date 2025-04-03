from pydantic import BaseModel, Field

from src.schemas.facilities import Facility


class RoomsAddRequests(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] | None = None


class RoomsAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class Rooms(RoomsAdd):
    id: int


class RoomWithRels(Rooms):
    facilities: list[Facility]


class RoomsPathRequests(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] | None = None


class RoomsPath(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
