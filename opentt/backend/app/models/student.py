from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class StudentYear(BaseModel):
    __tablename__ = "student_years"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    institution = relationship("Institution", back_populates="student_years")
    groups = relationship("StudentGroup", back_populates="year", cascade="all, delete-orphan", lazy="selectin")


class StudentGroup(BaseModel):
    __tablename__ = "student_groups"

    year_id = Column(Integer, ForeignKey("student_years.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    student_count = Column(Integer, default=0, nullable=False)

    year = relationship("StudentYear", back_populates="groups")
    subgroups = relationship("StudentSubgroup", back_populates="group", cascade="all, delete-orphan", lazy="selectin")
    activities = relationship("ActivityStudentGroup", back_populates="group", cascade="all, delete-orphan")


class StudentSubgroup(BaseModel):
    __tablename__ = "student_subgroups"

    group_id = Column(Integer, ForeignKey("student_groups.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    student_count = Column(Integer, default=0, nullable=False)

    group = relationship("StudentGroup", back_populates="subgroups")
    activities = relationship("ActivityStudentSubgroup", back_populates="subgroup", cascade="all, delete-orphan")
