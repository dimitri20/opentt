from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


# StudentYear schemas
class StudentYearCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    short_name: str = Field(..., min_length=1, max_length=20)
    order: int = Field(..., ge=0)


class StudentYearUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    short_name: Optional[str] = Field(None, min_length=1, max_length=20)
    order: Optional[int] = Field(None, ge=0)


class StudentYearRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    name: str
    short_name: str
    order: int
    created_at: datetime
    updated_at: datetime


# StudentGroup schemas
class StudentGroupCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    short_name: str = Field(..., min_length=1, max_length=20)
    student_count: int = Field(default=0, ge=0)


class StudentGroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    short_name: Optional[str] = Field(None, min_length=1, max_length=20)
    student_count: Optional[int] = Field(None, ge=0)


class StudentGroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    year_id: int
    name: str
    short_name: str
    student_count: int
    created_at: datetime
    updated_at: datetime


# StudentSubgroup schemas
class StudentSubgroupCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    short_name: str = Field(..., min_length=1, max_length=20)
    student_count: int = Field(default=0, ge=0)


class StudentSubgroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    short_name: Optional[str] = Field(None, min_length=1, max_length=20)
    student_count: Optional[int] = Field(None, ge=0)


class StudentSubgroupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: int
    name: str
    short_name: str
    student_count: int
    created_at: datetime
    updated_at: datetime


# Hierarchical schemas
class StudentGroupWithSubgroups(StudentGroupRead):
    subgroups: List[StudentSubgroupRead] = []


class StudentYearWithGroups(StudentYearRead):
    groups: List[StudentGroupWithSubgroups] = []
