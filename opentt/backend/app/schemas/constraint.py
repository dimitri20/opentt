from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# Teacher Constraints

class TeacherNotAvailableCreate(BaseModel):
    teacher_id: int
    day_id: int
    period_id: int
    is_hard: bool = True
    weight: int = Field(default=100, ge=0, le=100)


class TeacherNotAvailableUpdate(BaseModel):
    is_hard: Optional[bool] = None
    weight: Optional[int] = Field(None, ge=0, le=100)


class TeacherNotAvailableRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    day_id: int
    period_id: int
    is_hard: bool
    weight: int
    created_at: datetime
    updated_at: datetime


class TeacherMaxHoursDailyCreate(BaseModel):
    teacher_id: int
    max_hours: int = Field(..., ge=1, le=20)
    weight: int = Field(default=10, ge=0, le=100)


class TeacherMaxHoursDailyUpdate(BaseModel):
    max_hours: Optional[int] = Field(None, ge=1, le=20)
    weight: Optional[int] = Field(None, ge=0, le=100)


class TeacherMaxHoursDailyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    max_hours: int
    weight: int
    created_at: datetime
    updated_at: datetime


class TeacherMaxHoursWeeklyCreate(BaseModel):
    teacher_id: int
    max_hours: int = Field(..., ge=1, le=100)
    weight: int = Field(default=10, ge=0, le=100)


class TeacherMaxHoursWeeklyUpdate(BaseModel):
    max_hours: Optional[int] = Field(None, ge=1, le=100)
    weight: Optional[int] = Field(None, ge=0, le=100)


class TeacherMaxHoursWeeklyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    max_hours: int
    weight: int
    created_at: datetime
    updated_at: datetime


class TeacherMaxGapsDailyCreate(BaseModel):
    teacher_id: int
    max_gaps: int = Field(..., ge=0, le=20)
    weight: int = Field(default=5, ge=0, le=100)


class TeacherMaxGapsDailyUpdate(BaseModel):
    max_gaps: Optional[int] = Field(None, ge=0, le=20)
    weight: Optional[int] = Field(None, ge=0, le=100)


class TeacherMaxGapsDailyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    max_gaps: int
    weight: int
    created_at: datetime
    updated_at: datetime


class TeacherMaxGapsWeeklyCreate(BaseModel):
    teacher_id: int
    max_gaps: int = Field(..., ge=0, le=100)
    weight: int = Field(default=5, ge=0, le=100)


class TeacherMaxGapsWeeklyUpdate(BaseModel):
    max_gaps: Optional[int] = Field(None, ge=0, le=100)
    weight: Optional[int] = Field(None, ge=0, le=100)


class TeacherMaxGapsWeeklyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: int
    max_gaps: int
    weight: int
    created_at: datetime
    updated_at: datetime


# Student Constraints

class StudentsMaxHoursDailyCreate(BaseModel):
    group_id: Optional[int] = None
    subgroup_id: Optional[int] = None
    max_hours: int = Field(..., ge=1, le=20)
    weight: int = Field(default=10, ge=0, le=100)


class StudentsMaxHoursDailyUpdate(BaseModel):
    max_hours: Optional[int] = Field(None, ge=1, le=20)
    weight: Optional[int] = Field(None, ge=0, le=100)


class StudentsMaxHoursDailyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: Optional[int]
    subgroup_id: Optional[int]
    max_hours: int
    weight: int
    created_at: datetime
    updated_at: datetime


class StudentsMaxHoursWeeklyCreate(BaseModel):
    group_id: Optional[int] = None
    subgroup_id: Optional[int] = None
    max_hours: int = Field(..., ge=1, le=100)
    weight: int = Field(default=10, ge=0, le=100)


class StudentsMaxHoursWeeklyUpdate(BaseModel):
    max_hours: Optional[int] = Field(None, ge=1, le=100)
    weight: Optional[int] = Field(None, ge=0, le=100)


class StudentsMaxHoursWeeklyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: Optional[int]
    subgroup_id: Optional[int]
    max_hours: int
    weight: int
    created_at: datetime
    updated_at: datetime


class StudentsMaxGapsDailyCreate(BaseModel):
    group_id: Optional[int] = None
    subgroup_id: Optional[int] = None
    max_gaps: int = Field(..., ge=0, le=20)
    weight: int = Field(default=5, ge=0, le=100)


class StudentsMaxGapsDailyUpdate(BaseModel):
    max_gaps: Optional[int] = Field(None, ge=0, le=20)
    weight: Optional[int] = Field(None, ge=0, le=100)


class StudentsMaxGapsDailyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: Optional[int]
    subgroup_id: Optional[int]
    max_gaps: int
    weight: int
    created_at: datetime
    updated_at: datetime


class StudentsMaxGapsWeeklyCreate(BaseModel):
    group_id: Optional[int] = None
    subgroup_id: Optional[int] = None
    max_gaps: int = Field(..., ge=0, le=100)
    weight: int = Field(default=5, ge=0, le=100)


class StudentsMaxGapsWeeklyUpdate(BaseModel):
    max_gaps: Optional[int] = Field(None, ge=0, le=100)
    weight: Optional[int] = Field(None, ge=0, le=100)


class StudentsMaxGapsWeeklyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    group_id: Optional[int]
    subgroup_id: Optional[int]
    max_gaps: int
    weight: int
    created_at: datetime
    updated_at: datetime


# Activity Constraints

class ActivityPreferredStartingTimeCreate(BaseModel):
    activity_id: int
    day_id: int
    period_id: int
    weight: int = Field(default=10, ge=0, le=100)


class ActivityPreferredStartingTimeUpdate(BaseModel):
    weight: Optional[int] = Field(None, ge=0, le=100)


class ActivityPreferredStartingTimeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activity_id: int
    day_id: int
    period_id: int
    weight: int
    created_at: datetime
    updated_at: datetime


class ActivityPreferredStartingDayCreate(BaseModel):
    activity_id: int
    day_id: int
    weight: int = Field(default=10, ge=0, le=100)


class ActivityPreferredStartingDayUpdate(BaseModel):
    weight: Optional[int] = Field(None, ge=0, le=100)


class ActivityPreferredStartingDayRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activity_id: int
    day_id: int
    weight: int
    created_at: datetime
    updated_at: datetime


class ActivitiesNotOnSameDayCreate(BaseModel):
    activity1_id: int
    activity2_id: int
    weight: int = Field(default=10, ge=0, le=100)


class ActivitiesNotOnSameDayUpdate(BaseModel):
    weight: Optional[int] = Field(None, ge=0, le=100)


class ActivitiesNotOnSameDayRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activity1_id: int
    activity2_id: int
    weight: int
    created_at: datetime
    updated_at: datetime


class ActivitiesConsecutiveCreate(BaseModel):
    activity1_id: int
    activity2_id: int
    is_hard: bool = False
    weight: int = Field(default=10, ge=0, le=100)


class ActivitiesConsecutiveUpdate(BaseModel):
    is_hard: Optional[bool] = None
    weight: Optional[int] = Field(None, ge=0, le=100)


class ActivitiesConsecutiveRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activity1_id: int
    activity2_id: int
    is_hard: bool
    weight: int
    created_at: datetime
    updated_at: datetime


class ActivitiesSameStartingTimeCreate(BaseModel):
    activity1_id: int
    activity2_id: int
    is_hard: bool = False
    weight: int = Field(default=10, ge=0, le=100)


class ActivitiesSameStartingTimeUpdate(BaseModel):
    is_hard: Optional[bool] = None
    weight: Optional[int] = Field(None, ge=0, le=100)


class ActivitiesSameStartingTimeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activity1_id: int
    activity2_id: int
    is_hard: bool
    weight: int
    created_at: datetime
    updated_at: datetime


class ActivitiesSameStartingDayCreate(BaseModel):
    activity1_id: int
    activity2_id: int
    is_hard: bool = False
    weight: int = Field(default=10, ge=0, le=100)


class ActivitiesSameStartingDayUpdate(BaseModel):
    is_hard: Optional[bool] = None
    weight: Optional[int] = Field(None, ge=0, le=100)


class ActivitiesSameStartingDayRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    activity1_id: int
    activity2_id: int
    is_hard: bool
    weight: int
    created_at: datetime
    updated_at: datetime


# Room Constraints

class RoomNotAvailableCreate(BaseModel):
    room_id: int
    day_id: int
    period_id: int
    is_hard: bool = True
    weight: int = Field(default=100, ge=0, le=100)


class RoomNotAvailableUpdate(BaseModel):
    is_hard: Optional[bool] = None
    weight: Optional[int] = Field(None, ge=0, le=100)


class RoomNotAvailableRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    room_id: int
    day_id: int
    period_id: int
    is_hard: bool
    weight: int
    created_at: datetime
    updated_at: datetime
