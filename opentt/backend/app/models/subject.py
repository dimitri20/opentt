from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Subject(BaseModel):
    __tablename__ = "subjects"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    color = Column(String, default="#3B82F6", nullable=False)

    institution = relationship("Institution", back_populates="subjects")
    activities = relationship("Activity", back_populates="subject", cascade="all, delete-orphan")


class ActivityTag(BaseModel):
    __tablename__ = "activity_tags"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    color = Column(String, default="#6B7280", nullable=False)

    institution = relationship("Institution")
