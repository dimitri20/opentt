from app.models.base import BaseModel
from app.models.institution import Institution, AcademicYear, DayOfWeek, Period
from app.models.building import Building, Room
from app.models.subject import Subject, ActivityTag
from app.models.teacher import Teacher
from app.models.student import StudentYear, StudentGroup, StudentSubgroup
from app.models.activity import (
    Activity,
    ActivityTeacher,
    ActivityStudentGroup,
    ActivityStudentSubgroup,
    ActivityPreferredRoom,
)
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
from app.models.solve_job import SolveJob

__all__ = [
    "BaseModel",
    "Institution",
    "AcademicYear",
    "DayOfWeek",
    "Period",
    "Building",
    "Room",
    "Subject",
    "ActivityTag",
    "Teacher",
    "StudentYear",
    "StudentGroup",
    "StudentSubgroup",
    "Activity",
    "ActivityTeacher",
    "ActivityStudentGroup",
    "ActivityStudentSubgroup",
    "ActivityPreferredRoom",
    "TeacherNotAvailable",
    "TeacherMaxHoursDaily",
    "TeacherMaxHoursWeekly",
    "TeacherMaxGapsDaily",
    "TeacherMaxGapsWeekly",
    "StudentsMaxHoursDaily",
    "StudentsMaxHoursWeekly",
    "StudentsMaxGapsDaily",
    "StudentsMaxGapsWeekly",
    "ActivityPreferredStartingTime",
    "ActivityPreferredStartingDay",
    "ActivitiesNotOnSameDay",
    "ActivitiesConsecutive",
    "ActivitiesSameStartingTime",
    "ActivitiesSameStartingDay",
    "RoomNotAvailable",
    "SolveJob",
]
