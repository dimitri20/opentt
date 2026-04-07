from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class TeacherNotAvailable(BaseModel):
    __tablename__ = "constraint_teacher_not_available"

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    day_id = Column(Integer, ForeignKey("days_of_week.id", ondelete="CASCADE"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.id", ondelete="CASCADE"), nullable=False)
    is_hard = Column(Boolean, default=True, nullable=False)
    weight = Column(Integer, default=100, nullable=False)

    teacher = relationship("Teacher")
    day = relationship("DayOfWeek")
    period = relationship("Period")


class TeacherMaxHoursDaily(BaseModel):
    __tablename__ = "constraint_teacher_max_hours_daily"

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    max_hours = Column(Integer, nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    teacher = relationship("Teacher")


class TeacherMaxHoursWeekly(BaseModel):
    __tablename__ = "constraint_teacher_max_hours_weekly"

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    max_hours = Column(Integer, nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    teacher = relationship("Teacher")


class TeacherMaxGapsDaily(BaseModel):
    __tablename__ = "constraint_teacher_max_gaps_daily"

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    max_gaps = Column(Integer, nullable=False)
    weight = Column(Integer, default=5, nullable=False)

    teacher = relationship("Teacher")


class TeacherMaxGapsWeekly(BaseModel):
    __tablename__ = "constraint_teacher_max_gaps_weekly"

    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    max_gaps = Column(Integer, nullable=False)
    weight = Column(Integer, default=5, nullable=False)

    teacher = relationship("Teacher")
