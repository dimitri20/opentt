from sqlalchemy import Column, String, Integer, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.core.database import Base


activity_tag_association = Table(
    "activity_tag_association",
    Base.metadata,
    Column("activity_id", Integer, ForeignKey("activities.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("activity_tags.id", ondelete="CASCADE")),
)


class Activity(BaseModel):
    __tablename__ = "activities"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    duration = Column(Integer, default=1, nullable=False)
    split_count = Column(Integer, default=1, nullable=False)
    total_student_count = Column(Integer, default=0, nullable=False)
    requires_room = Column(Boolean, default=True, nullable=False)

    institution = relationship("Institution", back_populates="activities")
    subject = relationship("Subject", back_populates="activities")
    teachers = relationship("ActivityTeacher", back_populates="activity", cascade="all, delete-orphan", lazy="selectin")
    student_groups = relationship("ActivityStudentGroup", back_populates="activity", cascade="all, delete-orphan", lazy="selectin")
    student_subgroups = relationship("ActivityStudentSubgroup", back_populates="activity", cascade="all, delete-orphan", lazy="selectin")
    preferred_rooms = relationship("ActivityPreferredRoom", back_populates="activity", cascade="all, delete-orphan", lazy="selectin")
    tags = relationship("ActivityTag", secondary=activity_tag_association, lazy="selectin")


class ActivityTeacher(BaseModel):
    __tablename__ = "activity_teachers"

    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)

    activity = relationship("Activity", back_populates="teachers")
    teacher = relationship("Teacher", back_populates="activities")


class ActivityStudentGroup(BaseModel):
    __tablename__ = "activity_student_groups"

    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(Integer, ForeignKey("student_groups.id", ondelete="CASCADE"), nullable=False)

    activity = relationship("Activity", back_populates="student_groups")
    group = relationship("StudentGroup", back_populates="activities")


class ActivityStudentSubgroup(BaseModel):
    __tablename__ = "activity_student_subgroups"

    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    subgroup_id = Column(Integer, ForeignKey("student_subgroups.id", ondelete="CASCADE"), nullable=False)

    activity = relationship("Activity", back_populates="student_subgroups")
    subgroup = relationship("StudentSubgroup", back_populates="activities")


class ActivityPreferredRoom(BaseModel):
    __tablename__ = "activity_preferred_rooms"

    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    priority = Column(Integer, default=1, nullable=False)

    activity = relationship("Activity", back_populates="preferred_rooms")
    room = relationship("Room", back_populates="preferred_activities")
