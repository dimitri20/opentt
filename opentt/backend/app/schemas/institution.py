from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


# Institution schemas
class InstitutionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")
    timezone: str = Field(default="UTC", max_length=50)
    description: Optional[str] = None


class InstitutionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    timezone: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class InstitutionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    timezone: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


# AcademicYear schemas
class AcademicYearCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    start_year: int = Field(..., ge=2000, le=2100)
    end_year: int = Field(..., ge=2000, le=2100)
    is_active: bool = False


class AcademicYearUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    start_year: Optional[int] = Field(None, ge=2000, le=2100)
    end_year: Optional[int] = Field(None, ge=2000, le=2100)
    is_active: Optional[bool] = None


class AcademicYearRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    name: str
    start_year: int
    end_year: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


# DayOfWeek schemas
class DayOfWeekCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    short_name: str = Field(..., min_length=1, max_length=10)
    order: int = Field(..., ge=0)
    is_active: bool = True


class DayOfWeekUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    short_name: Optional[str] = Field(None, min_length=1, max_length=10)
    order: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class DayOfWeekRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    name: str
    short_name: str
    order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


# Period schemas
class PeriodCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    start_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    end_time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    order: int = Field(..., ge=0)


class PeriodUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    start_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    end_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    order: Optional[int] = Field(None, ge=0)


class PeriodRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    name: str
    start_time: str
    end_time: str
    order: int
    created_at: datetime
    updated_at: datetime
