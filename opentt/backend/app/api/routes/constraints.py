from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.services.constraint_service import *
from app.schemas.constraint import *

router = APIRouter()


# Teacher Constraints - Not Available
@router.post("/{institution_id}/constraints/teacher-not-available", response_model=TeacherNotAvailableRead, status_code=status.HTTP_201_CREATED)
async def create_teacher_not_available(
    institution_id: int,
    constraint: TeacherNotAvailableCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create teacher not available constraint"""
    return await teacher_not_available_service.create(db, obj_in=constraint)


@router.get("/{institution_id}/constraints/teacher-not-available", response_model=List[TeacherNotAvailableRead])
async def list_teacher_not_available(
    institution_id: int, teacher_id: int = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List teacher not available constraints"""
    filters = {}
    if teacher_id:
        filters["teacher_id"] = teacher_id
    return await teacher_not_available_service.get_multi(db, skip=skip, limit=limit, filters=filters)


@router.delete("/{institution_id}/constraints/teacher-not-available/{constraint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher_not_available(
    institution_id: int, constraint_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete teacher not available constraint"""
    await teacher_not_available_service.delete(db, id=constraint_id)


# Teacher Max Hours Daily
@router.post("/{institution_id}/constraints/teacher-max-hours-daily", response_model=TeacherMaxHoursDailyRead, status_code=status.HTTP_201_CREATED)
async def create_teacher_max_hours_daily(
    institution_id: int,
    constraint: TeacherMaxHoursDailyCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create teacher max hours daily constraint"""
    return await teacher_max_hours_daily_service.create(db, obj_in=constraint)


@router.get("/{institution_id}/constraints/teacher-max-hours-daily", response_model=List[TeacherMaxHoursDailyRead])
async def list_teacher_max_hours_daily(
    institution_id: int, teacher_id: int = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List teacher max hours daily constraints"""
    filters = {}
    if teacher_id:
        filters["teacher_id"] = teacher_id
    return await teacher_max_hours_daily_service.get_multi(db, skip=skip, limit=limit, filters=filters)


@router.delete("/{institution_id}/constraints/teacher-max-hours-daily/{constraint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher_max_hours_daily(
    institution_id: int, constraint_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete teacher max hours daily constraint"""
    await teacher_max_hours_daily_service.delete(db, id=constraint_id)


# Teacher Max Hours Weekly
@router.post("/{institution_id}/constraints/teacher-max-hours-weekly", response_model=TeacherMaxHoursWeeklyRead, status_code=status.HTTP_201_CREATED)
async def create_teacher_max_hours_weekly(
    institution_id: int,
    constraint: TeacherMaxHoursWeeklyCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create teacher max hours weekly constraint"""
    return await teacher_max_hours_weekly_service.create(db, obj_in=constraint)


@router.get("/{institution_id}/constraints/teacher-max-hours-weekly", response_model=List[TeacherMaxHoursWeeklyRead])
async def list_teacher_max_hours_weekly(
    institution_id: int, teacher_id: int = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List teacher max hours weekly constraints"""
    filters = {}
    if teacher_id:
        filters["teacher_id"] = teacher_id
    return await teacher_max_hours_weekly_service.get_multi(db, skip=skip, limit=limit, filters=filters)


@router.delete("/{institution_id}/constraints/teacher-max-hours-weekly/{constraint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher_max_hours_weekly(
    institution_id: int, constraint_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete teacher max hours weekly constraint"""
    await teacher_max_hours_weekly_service.delete(db, id=constraint_id)


# Student Max Hours Daily
@router.post("/{institution_id}/constraints/students-max-hours-daily", response_model=StudentsMaxHoursDailyRead, status_code=status.HTTP_201_CREATED)
async def create_students_max_hours_daily(
    institution_id: int,
    constraint: StudentsMaxHoursDailyCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create students max hours daily constraint"""
    return await students_max_hours_daily_service.create(db, obj_in=constraint)


@router.get("/{institution_id}/constraints/students-max-hours-daily", response_model=List[StudentsMaxHoursDailyRead])
async def list_students_max_hours_daily(
    institution_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List students max hours daily constraints"""
    return await students_max_hours_daily_service.get_multi(db, skip=skip, limit=limit)


@router.delete("/{institution_id}/constraints/students-max-hours-daily/{constraint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_students_max_hours_daily(
    institution_id: int, constraint_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete students max hours daily constraint"""
    await students_max_hours_daily_service.delete(db, id=constraint_id)


# Activity Preferred Starting Time
@router.post("/{institution_id}/constraints/activity-preferred-time", response_model=ActivityPreferredStartingTimeRead, status_code=status.HTTP_201_CREATED)
async def create_activity_preferred_time(
    institution_id: int,
    constraint: ActivityPreferredStartingTimeCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create activity preferred starting time constraint"""
    return await activity_preferred_starting_time_service.create(db, obj_in=constraint)


@router.get("/{institution_id}/constraints/activity-preferred-time", response_model=List[ActivityPreferredStartingTimeRead])
async def list_activity_preferred_time(
    institution_id: int, activity_id: int = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List activity preferred starting time constraints"""
    filters = {}
    if activity_id:
        filters["activity_id"] = activity_id
    return await activity_preferred_starting_time_service.get_multi(db, skip=skip, limit=limit, filters=filters)


@router.delete("/{institution_id}/constraints/activity-preferred-time/{constraint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity_preferred_time(
    institution_id: int, constraint_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete activity preferred starting time constraint"""
    await activity_preferred_starting_time_service.delete(db, id=constraint_id)


# Activities Consecutive
@router.post("/{institution_id}/constraints/activities-consecutive", response_model=ActivitiesConsecutiveRead, status_code=status.HTTP_201_CREATED)
async def create_activities_consecutive(
    institution_id: int,
    constraint: ActivitiesConsecutiveCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create activities consecutive constraint"""
    return await activities_consecutive_service.create(db, obj_in=constraint)


@router.get("/{institution_id}/constraints/activities-consecutive", response_model=List[ActivitiesConsecutiveRead])
async def list_activities_consecutive(
    institution_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List activities consecutive constraints"""
    return await activities_consecutive_service.get_multi(db, skip=skip, limit=limit)


@router.delete("/{institution_id}/constraints/activities-consecutive/{constraint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activities_consecutive(
    institution_id: int, constraint_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete activities consecutive constraint"""
    await activities_consecutive_service.delete(db, id=constraint_id)


# Room Not Available
@router.post("/{institution_id}/constraints/room-not-available", response_model=RoomNotAvailableRead, status_code=status.HTTP_201_CREATED)
async def create_room_not_available(
    institution_id: int,
    constraint: RoomNotAvailableCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create room not available constraint"""
    return await room_not_available_service.create(db, obj_in=constraint)


@router.get("/{institution_id}/constraints/room-not-available", response_model=List[RoomNotAvailableRead])
async def list_room_not_available(
    institution_id: int, room_id: int = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List room not available constraints"""
    filters = {}
    if room_id:
        filters["room_id"] = room_id
    return await room_not_available_service.get_multi(db, skip=skip, limit=limit, filters=filters)


@router.delete("/{institution_id}/constraints/room-not-available/{constraint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room_not_available(
    institution_id: int, constraint_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete room not available constraint"""
    await room_not_available_service.delete(db, id=constraint_id)


# Get all constraints for an institution (aggregated endpoint)
@router.get("/{institution_id}/constraints/all")
async def get_all_constraints(institution_id: int, db: AsyncSession = Depends(get_db)):
    """Get all constraints for an institution (for solver)"""
    # This endpoint will be used by the solver to load all constraints
    return {
        "teacher_not_available": await teacher_not_available_service.get_multi(db, limit=1000),
        "teacher_max_hours_daily": await teacher_max_hours_daily_service.get_multi(db, limit=1000),
        "teacher_max_hours_weekly": await teacher_max_hours_weekly_service.get_multi(db, limit=1000),
        "students_max_hours_daily": await students_max_hours_daily_service.get_multi(db, limit=1000),
        "activity_preferred_time": await activity_preferred_starting_time_service.get_multi(db, limit=1000),
        "activities_consecutive": await activities_consecutive_service.get_multi(db, limit=1000),
        "room_not_available": await room_not_available_service.get_multi(db, limit=1000),
    }
