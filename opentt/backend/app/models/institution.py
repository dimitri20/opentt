from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Institution(BaseModel):
    __tablename__ = "institutions"

    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    timezone = Column(String, default="UTC", nullable=False)
    description = Column(String, nullable=True)

    academic_years = relationship("AcademicYear", back_populates="institution", cascade="all, delete-orphan", lazy="selectin")
    days_of_week = relationship("DayOfWeek", back_populates="institution", cascade="all, delete-orphan", lazy="selectin")
    periods = relationship("Period", back_populates="institution", cascade="all, delete-orphan", lazy="selectin")
    buildings = relationship("Building", back_populates="institution", cascade="all, delete-orphan")
    teachers = relationship("Teacher", back_populates="institution", cascade="all, delete-orphan")
    subjects = relationship("Subject", back_populates="institution", cascade="all, delete-orphan")
    student_years = relationship("StudentYear", back_populates="institution", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="institution", cascade="all, delete-orphan")
    solve_jobs = relationship("SolveJob", back_populates="institution", cascade="all, delete-orphan")


class AcademicYear(BaseModel):
    __tablename__ = "academic_years"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)

    institution = relationship("Institution", back_populates="academic_years")


class DayOfWeek(BaseModel):
    __tablename__ = "days_of_week"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    institution = relationship("Institution", back_populates="days_of_week")


class Period(BaseModel):
    __tablename__ = "periods"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    institution = relationship("Institution", back_populates="periods")
