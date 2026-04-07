from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr


# Teacher schemas
class TeacherCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    code: Optional[str] = Field(None, max_length=50)
    color: str = Field(default="#10B981", pattern=r"^#[0-9A-Fa-f]{6}$")


class TeacherUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    code: Optional[str] = Field(None, max_length=50)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")


class TeacherRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    first_name: str
    last_name: str
    email: Optional[str]
    code: Optional[str]
    color: str
    created_at: datetime
    updated_at: datetime
