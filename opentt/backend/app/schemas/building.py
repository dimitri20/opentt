from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


# Building schemas
class BuildingCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=500)


class BuildingUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = Field(None, max_length=500)


class BuildingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    name: str
    code: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime


# Room schemas
class RoomCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    capacity: int = Field(default=0, ge=0)
    room_type: Optional[str] = Field(None, max_length=50)


class RoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    capacity: Optional[int] = Field(None, ge=0)
    room_type: Optional[str] = Field(None, max_length=50)


class RoomRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    building_id: int
    name: str
    code: Optional[str]
    capacity: int
    room_type: Optional[str]
    created_at: datetime
    updated_at: datetime


# Building with rooms
class BuildingWithRooms(BuildingRead):
    rooms: List[RoomRead] = []
