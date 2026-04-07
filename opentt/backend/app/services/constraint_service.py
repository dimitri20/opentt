from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.constraint_teacher import (
    TeacherNotAvailable,
    TeacherMaxHoursDaily,
    TeacherMaxHoursWeekly,
    TeacherMaxGapsDaily,
    TeacherMaxGapsWeekly,
)
from app.models.constraint_student import (
    StudentsMaxHoursDaily,
    StudentsMaxHoursWeekly,
    StudentsMaxGapsDaily,
    StudentsMaxGapsWeekly,
)
from app.models.constraint_activity import (
    ActivityPreferredStartingTime,
    ActivityPreferredStartingDay,
    ActivitiesNotOnSameDay,
    ActivitiesConsecutive,
    ActivitiesSameStartingTime,
    ActivitiesSameStartingDay,
)
from app.models.constraint_room import RoomNotAvailable
from app.schemas.constraint import *
from app.services.base import BaseService


# Teacher Constraint Services
class TeacherNotAvailableService(
    BaseService[TeacherNotAvailable, TeacherNotAvailableCreate, TeacherNotAvailableUpdate]
):
    def __init__(self):
        super().__init__(TeacherNotAvailable)


class TeacherMaxHoursDailyService(
    BaseService[TeacherMaxHoursDaily, TeacherMaxHoursDailyCreate, TeacherMaxHoursDailyUpdate]
):
    def __init__(self):
        super().__init__(TeacherMaxHoursDaily)


class TeacherMaxHoursWeeklyService(
    BaseService[TeacherMaxHoursWeekly, TeacherMaxHoursWeeklyCreate, TeacherMaxHoursWeeklyUpdate]
):
    def __init__(self):
        super().__init__(TeacherMaxHoursWeekly)


class TeacherMaxGapsDailyService(
    BaseService[TeacherMaxGapsDaily, TeacherMaxGapsDailyCreate, TeacherMaxGapsDailyUpdate]
):
    def __init__(self):
        super().__init__(TeacherMaxGapsDaily)


class TeacherMaxGapsWeeklyService(
    BaseService[TeacherMaxGapsWeekly, TeacherMaxGapsWeeklyCreate, TeacherMaxGapsWeeklyUpdate]
):
    def __init__(self):
        super().__init__(TeacherMaxGapsWeekly)


# Student Constraint Services
class StudentsMaxHoursDailyService(
    BaseService[StudentsMaxHoursDaily, StudentsMaxHoursDailyCreate, StudentsMaxHoursDailyUpdate]
):
    def __init__(self):
        super().__init__(StudentsMaxHoursDaily)


class StudentsMaxHoursWeeklyService(
    BaseService[StudentsMaxHoursWeekly, StudentsMaxHoursWeeklyCreate, StudentsMaxHoursWeeklyUpdate]
):
    def __init__(self):
        super().__init__(StudentsMaxHoursWeekly)


class StudentsMaxGapsDailyService(
    BaseService[StudentsMaxGapsDaily, StudentsMaxGapsDailyCreate, StudentsMaxGapsDailyUpdate]
):
    def __init__(self):
        super().__init__(StudentsMaxGapsDaily)


class StudentsMaxGapsWeeklyService(
    BaseService[StudentsMaxGapsWeekly, StudentsMaxGapsWeeklyCreate, StudentsMaxGapsWeeklyUpdate]
):
    def __init__(self):
        super().__init__(StudentsMaxGapsWeekly)


# Activity Constraint Services
class ActivityPreferredStartingTimeService(
    BaseService[
        ActivityPreferredStartingTime,
        ActivityPreferredStartingTimeCreate,
        ActivityPreferredStartingTimeUpdate,
    ]
):
    def __init__(self):
        super().__init__(ActivityPreferredStartingTime)


class ActivityPreferredStartingDayService(
    BaseService[
        ActivityPreferredStartingDay,
        ActivityPreferredStartingDayCreate,
        ActivityPreferredStartingDayUpdate,
    ]
):
    def __init__(self):
        super().__init__(ActivityPreferredStartingDay)


class ActivitiesNotOnSameDayService(
    BaseService[
        ActivitiesNotOnSameDay, ActivitiesNotOnSameDayCreate, ActivitiesNotOnSameDayUpdate
    ]
):
    def __init__(self):
        super().__init__(ActivitiesNotOnSameDay)


class ActivitiesConsecutiveService(
    BaseService[ActivitiesConsecutive, ActivitiesConsecutiveCreate, ActivitiesConsecutiveUpdate]
):
    def __init__(self):
        super().__init__(ActivitiesConsecutive)


class ActivitiesSameStartingTimeService(
    BaseService[
        ActivitiesSameStartingTime,
        ActivitiesSameStartingTimeCreate,
        ActivitiesSameStartingTimeUpdate,
    ]
):
    def __init__(self):
        super().__init__(ActivitiesSameStartingTime)


class ActivitiesSameStartingDayService(
    BaseService[
        ActivitiesSameStartingDay,
        ActivitiesSameStartingDayCreate,
        ActivitiesSameStartingDayUpdate,
    ]
):
    def __init__(self):
        super().__init__(ActivitiesSameStartingDay)


# Room Constraint Services
class RoomNotAvailableService(
    BaseService[RoomNotAvailable, RoomNotAvailableCreate, RoomNotAvailableUpdate]
):
    def __init__(self):
        super().__init__(RoomNotAvailable)


# Service instances
teacher_not_available_service = TeacherNotAvailableService()
teacher_max_hours_daily_service = TeacherMaxHoursDailyService()
teacher_max_hours_weekly_service = TeacherMaxHoursWeeklyService()
teacher_max_gaps_daily_service = TeacherMaxGapsDailyService()
teacher_max_gaps_weekly_service = TeacherMaxGapsWeeklyService()

students_max_hours_daily_service = StudentsMaxHoursDailyService()
students_max_hours_weekly_service = StudentsMaxHoursWeeklyService()
students_max_gaps_daily_service = StudentsMaxGapsDailyService()
students_max_gaps_weekly_service = StudentsMaxGapsWeeklyService()

activity_preferred_starting_time_service = ActivityPreferredStartingTimeService()
activity_preferred_starting_day_service = ActivityPreferredStartingDayService()
activities_not_on_same_day_service = ActivitiesNotOnSameDayService()
activities_consecutive_service = ActivitiesConsecutiveService()
activities_same_starting_time_service = ActivitiesSameStartingTimeService()
activities_same_starting_day_service = ActivitiesSameStartingDayService()

room_not_available_service = RoomNotAvailableService()
