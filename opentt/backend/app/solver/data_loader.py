from dataclasses import dataclass, field
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.institution import DayOfWeek, Period
from app.models.building import Room
from app.models.teacher import Teacher
from app.models.student import StudentGroup, StudentSubgroup
from app.models.activity import Activity, ActivityTeacher, ActivityStudentGroup, ActivityStudentSubgroup
from app.models.constraint_teacher import (
    TeacherNotAvailable,
    TeacherMaxHoursDaily,
    TeacherMaxHoursWeekly,
)
from app.models.constraint_student import StudentsMaxHoursDaily
from app.models.constraint_room import RoomNotAvailable


@dataclass
class DayData:
    id: int
    name: str
    short_name: str
    order: int


@dataclass
class PeriodData:
    id: int
    name: str
    start_time: str
    end_time: str
    order: int


@dataclass
class RoomData:
    id: int
    name: str
    capacity: int
    building_id: int


@dataclass
class TeacherData:
    id: int
    name: str


@dataclass
class StudentGroupData:
    id: int
    name: str
    student_count: int


@dataclass
class ActivityData:
    id: int
    name: str
    subject_id: int
    duration: int
    split_count: int
    total_student_count: int
    requires_room: bool
    teacher_ids: List[int]
    group_ids: List[int]
    subgroup_ids: List[int]
    preferred_room_ids: List[int]


@dataclass
class TeacherNotAvailableData:
    teacher_id: int
    day_id: int
    period_id: int
    is_hard: bool
    weight: int


@dataclass
class RoomNotAvailableData:
    room_id: int
    day_id: int
    period_id: int
    is_hard: bool
    weight: int


@dataclass
class TeacherMaxHoursDailyData:
    teacher_id: int
    max_hours: int
    weight: int


@dataclass
class ConstraintData:
    teacher_not_available: List[TeacherNotAvailableData] = field(default_factory=list)
    teacher_max_hours_daily: List[TeacherMaxHoursDailyData] = field(default_factory=list)
    room_not_available: List[RoomNotAvailableData] = field(default_factory=list)


@dataclass
class InstitutionData:
    institution_id: int
    days: List[DayData]
    periods: List[PeriodData]
    rooms: List[RoomData]
    teachers: List[TeacherData]
    student_groups: List[StudentGroupData]
    activities: List[ActivityData]
    constraints: ConstraintData


async def load_institution_data(
    institution_id: int, db: AsyncSession
) -> InstitutionData:
    """Load all data needed for timetable solving"""
    
    # Load days
    days_result = await db.execute(
        select(DayOfWeek)
        .where(DayOfWeek.institution_id == institution_id)
        .where(DayOfWeek.is_active == True)
        .order_by(DayOfWeek.order)
    )
    days = [
        DayData(
            id=d.id,
            name=d.name,
            short_name=d.short_name,
            order=d.order,
        )
        for d in days_result.scalars().all()
    ]
    
    # Load periods
    periods_result = await db.execute(
        select(Period)
        .where(Period.institution_id == institution_id)
        .order_by(Period.order)
    )
    periods = [
        PeriodData(
            id=p.id,
            name=p.name,
            start_time=p.start_time,
            end_time=p.end_time,
            order=p.order,
        )
        for p in periods_result.scalars().all()
    ]
    
    # Load rooms with building info
    rooms_result = await db.execute(
        select(Room)
        .join(Room.building)
        .where(Room.building.has(institution_id=institution_id))
    )
    rooms = [
        RoomData(
            id=r.id,
            name=r.name,
            capacity=r.capacity,
            building_id=r.building_id,
        )
        for r in rooms_result.scalars().all()
    ]
    
    # Load teachers
    teachers_result = await db.execute(
        select(Teacher).where(Teacher.institution_id == institution_id)
    )
    teachers = [
        TeacherData(
            id=t.id,
            name=f"{t.first_name} {t.last_name}",
        )
        for t in teachers_result.scalars().all()
    ]
    
    # Load student groups
    groups_result = await db.execute(
        select(StudentGroup)
        .join(StudentGroup.year)
        .where(StudentGroup.year.has(institution_id=institution_id))
    )
    student_groups = [
        StudentGroupData(
            id=g.id,
            name=g.name,
            student_count=g.student_count,
        )
        for g in groups_result.scalars().all()
    ]
    
    # Load activities with relationships
    activities_result = await db.execute(
        select(Activity)
        .where(Activity.institution_id == institution_id)
        .options(
            selectinload(Activity.teachers).selectinload(ActivityTeacher.teacher),
            selectinload(Activity.student_groups).selectinload(ActivityStudentGroup.group),
            selectinload(Activity.student_subgroups).selectinload(ActivityStudentSubgroup.subgroup),
        )
    )
    activities = []
    for a in activities_result.scalars().all():
        teacher_ids = [at.teacher_id for at in a.teachers]
        group_ids = [ag.group_id for ag in a.student_groups]
        subgroup_ids = [asg.subgroup_id for asg in a.student_subgroups]
        
        # Get preferred rooms (would need to load from ActivityPreferredRoom)
        preferred_room_ids = []
        
        activities.append(
            ActivityData(
                id=a.id,
                name=a.name,
                subject_id=a.subject_id,
                duration=a.duration,
                split_count=a.split_count,
                total_student_count=a.total_student_count,
                requires_room=a.requires_room,
                teacher_ids=teacher_ids,
                group_ids=group_ids,
                subgroup_ids=subgroup_ids,
                preferred_room_ids=preferred_room_ids,
            )
        )
    
    # Load constraints
    teacher_not_available_result = await db.execute(
        select(TeacherNotAvailable)
        .join(TeacherNotAvailable.teacher)
        .where(TeacherNotAvailable.teacher.has(institution_id=institution_id))
    )
    teacher_not_available = [
        TeacherNotAvailableData(
            teacher_id=c.teacher_id,
            day_id=c.day_id,
            period_id=c.period_id,
            is_hard=c.is_hard,
            weight=c.weight,
        )
        for c in teacher_not_available_result.scalars().all()
    ]
    
    teacher_max_hours_daily_result = await db.execute(
        select(TeacherMaxHoursDaily)
        .join(TeacherMaxHoursDaily.teacher)
        .where(TeacherMaxHoursDaily.teacher.has(institution_id=institution_id))
    )
    teacher_max_hours_daily = [
        TeacherMaxHoursDailyData(
            teacher_id=c.teacher_id,
            max_hours=c.max_hours,
            weight=c.weight,
        )
        for c in teacher_max_hours_daily_result.scalars().all()
    ]
    
    room_not_available_result = await db.execute(
        select(RoomNotAvailable)
        .join(RoomNotAvailable.room)
        .join(Room.building)
        .where(Room.building.has(institution_id=institution_id))
    )
    room_not_available = [
        RoomNotAvailableData(
            room_id=c.room_id,
            day_id=c.day_id,
            period_id=c.period_id,
            is_hard=c.is_hard,
            weight=c.weight,
        )
        for c in room_not_available_result.scalars().all()
    ]
    
    constraints = ConstraintData(
        teacher_not_available=teacher_not_available,
        teacher_max_hours_daily=teacher_max_hours_daily,
        room_not_available=room_not_available,
    )
    
    return InstitutionData(
        institution_id=institution_id,
        days=days,
        periods=periods,
        rooms=rooms,
        teachers=teachers,
        student_groups=student_groups,
        activities=activities,
        constraints=constraints,
    )
