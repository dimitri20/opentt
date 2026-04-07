from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class StudentsMaxHoursDaily(BaseModel):
    __tablename__ = "constraint_students_max_hours_daily"

    group_id = Column(Integer, ForeignKey("student_groups.id", ondelete="CASCADE"), nullable=True)
    subgroup_id = Column(Integer, ForeignKey("student_subgroups.id", ondelete="CASCADE"), nullable=True)
    max_hours = Column(Integer, nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    group = relationship("StudentGroup")
    subgroup = relationship("StudentSubgroup")


class StudentsMaxHoursWeekly(BaseModel):
    __tablename__ = "constraint_students_max_hours_weekly"

    group_id = Column(Integer, ForeignKey("student_groups.id", ondelete="CASCADE"), nullable=True)
    subgroup_id = Column(Integer, ForeignKey("student_subgroups.id", ondelete="CASCADE"), nullable=True)
    max_hours = Column(Integer, nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    group = relationship("StudentGroup")
    subgroup = relationship("StudentSubgroup")


class StudentsMaxGapsDaily(BaseModel):
    __tablename__ = "constraint_students_max_gaps_daily"

    group_id = Column(Integer, ForeignKey("student_groups.id", ondelete="CASCADE"), nullable=True)
    subgroup_id = Column(Integer, ForeignKey("student_subgroups.id", ondelete="CASCADE"), nullable=True)
    max_gaps = Column(Integer, nullable=False)
    weight = Column(Integer, default=5, nullable=False)

    group = relationship("StudentGroup")
    subgroup = relationship("StudentSubgroup")


class StudentsMaxGapsWeekly(BaseModel):
    __tablename__ = "constraint_students_max_gaps_weekly"

    group_id = Column(Integer, ForeignKey("student_groups.id", ondelete="CASCADE"), nullable=True)
    subgroup_id = Column(Integer, ForeignKey("student_subgroups.id", ondelete="CASCADE"), nullable=True)
    max_gaps = Column(Integer, nullable=False)
    weight = Column(Integer, default=5, nullable=False)

    group = relationship("StudentGroup")
    subgroup = relationship("StudentSubgroup")
