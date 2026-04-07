from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


# Activity schemas
class ActivityCreate(BaseModel):
    subject_id: int
    name: str = Field(..., min_length=1, max_length=255)
    duration: int = Field(default=1, ge=1, le=10)
    split_count: int = Field(default=1, ge=1, le=10)
    total_student_count: int = Field(default=0, ge=0)
    requires_room: bool = True
    teacher_ids: List[int] = []
    group_ids: List[int] = []
    subgroup_ids: List[int] = []
    preferred_room_ids: List[int] = []
    tag_ids: List[int] = []


class ActivityUpdate(BaseModel):
    subject_id: Optional[int] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    duration: Optional[int] = Field(None, ge=1, le=10)
    split_count: Optional[int] = Field(None, ge=1, le=10)
    total_student_count: Optional[int] = Field(None, ge=0)
    requires_room: Optional[bool] = None
    teacher_ids: Optional[List[int]] = None
    group_ids: Optional[List[int]] = None
    subgroup_ids: Optional[List[int]] = None
    preferred_room_ids: Optional[List[int]] = None
    tag_ids: Optional[List[int]] = None


class ActivityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    subject_id: int
    name: str
    duration: int
    split_count: int
    total_student_count: int
    requires_room: bool
    created_at: datetime
    updated_at: datetime


# Forward references for related schemas
from app.schemas.teacher import TeacherRead
from app.schemas.student import StudentGroupRead, StudentSubgroupRead
from app.schemas.building import RoomRead
from app.schemas.subject import SubjectRead, ActivityTagRead


# Activity with full relationships
class ActivityWithRelations(ActivityRead):
    subject: Optional[SubjectRead] = None
    teachers: List[TeacherRead] = []
    groups: List[StudentGroupRead] = []
    subgroups: List[StudentSubgroupRead] = []
    preferred_rooms: List[RoomRead] = []
    tags: List[ActivityTagRead] = []
