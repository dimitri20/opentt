from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.building import Building, Room
from app.models.subject import Subject, ActivityTag
from app.models.teacher import Teacher
from app.models.student import StudentYear, StudentGroup, StudentSubgroup
from app.schemas.building import BuildingCreate, BuildingUpdate, RoomCreate, RoomUpdate
from app.schemas.subject import SubjectCreate, SubjectUpdate, ActivityTagCreate, ActivityTagUpdate
from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.schemas.student import (
    StudentYearCreate,
    StudentYearUpdate,
    StudentGroupCreate,
    StudentGroupUpdate,
    StudentSubgroupCreate,
    StudentSubgroupUpdate,
)
from app.services.base import BaseService


# Building Service
class BuildingService(BaseService[Building, BuildingCreate, BuildingUpdate]):
    def __init__(self):
        super().__init__(Building)

    async def get_with_rooms(self, db: AsyncSession, building_id: int) -> Optional[Building]:
        """Get building with all its rooms"""
        result = await db.execute(
            select(Building)
            .where(Building.id == building_id)
            .options(selectinload(Building.rooms))
        )
        return result.scalar_one_or_none()


# Room Service
class RoomService(BaseService[Room, RoomCreate, RoomUpdate]):
    def __init__(self):
        super().__init__(Room)

    async def get_by_building(self, db: AsyncSession, building_id: int) -> List[Room]:
        """Get all rooms in a building"""
        result = await db.execute(select(Room).where(Room.building_id == building_id))
        return list(result.scalars().all())


# Subject Service
class SubjectService(BaseService[Subject, SubjectCreate, SubjectUpdate]):
    def __init__(self):
        super().__init__(Subject)


# ActivityTag Service
class ActivityTagService(BaseService[ActivityTag, ActivityTagCreate, ActivityTagUpdate]):
    def __init__(self):
        super().__init__(ActivityTag)


# Teacher Service
class TeacherService(BaseService[Teacher, TeacherCreate, TeacherUpdate]):
    def __init__(self):
        super().__init__(Teacher)


# StudentYear Service
class StudentYearService(BaseService[StudentYear, StudentYearCreate, StudentYearUpdate]):
    def __init__(self):
        super().__init__(StudentYear)

    async def get_with_groups(self, db: AsyncSession, year_id: int) -> Optional[StudentYear]:
        """Get year with all groups and subgroups"""
        result = await db.execute(
            select(StudentYear)
            .where(StudentYear.id == year_id)
            .options(
                selectinload(StudentYear.groups).selectinload(StudentGroup.subgroups)
            )
        )
        return result.scalar_one_or_none()


# StudentGroup Service
class StudentGroupService(BaseService[StudentGroup, StudentGroupCreate, StudentGroupUpdate]):
    def __init__(self):
        super().__init__(StudentGroup)

    async def get_with_subgroups(self, db: AsyncSession, group_id: int) -> Optional[StudentGroup]:
        """Get group with all subgroups"""
        result = await db.execute(
            select(StudentGroup)
            .where(StudentGroup.id == group_id)
            .options(selectinload(StudentGroup.subgroups))
        )
        return result.scalar_one_or_none()

    async def get_by_year(self, db: AsyncSession, year_id: int) -> List[StudentGroup]:
        """Get all groups in a year"""
        result = await db.execute(
            select(StudentGroup)
            .where(StudentGroup.year_id == year_id)
            .options(selectinload(StudentGroup.subgroups))
        )
        return list(result.scalars().all())


# StudentSubgroup Service
class StudentSubgroupService(BaseService[StudentSubgroup, StudentSubgroupCreate, StudentSubgroupUpdate]):
    def __init__(self):
        super().__init__(StudentSubgroup)

    async def get_by_group(self, db: AsyncSession, group_id: int) -> List[StudentSubgroup]:
        """Get all subgroups in a group"""
        result = await db.execute(
            select(StudentSubgroup).where(StudentSubgroup.group_id == group_id)
        )
        return list(result.scalars().all())


# Service instances
building_service = BuildingService()
room_service = RoomService()
subject_service = SubjectService()
activity_tag_service = ActivityTagService()
teacher_service = TeacherService()
student_year_service = StudentYearService()
student_group_service = StudentGroupService()
student_subgroup_service = StudentSubgroupService()
