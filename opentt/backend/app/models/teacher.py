from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Teacher(BaseModel):
    __tablename__ = "teachers"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    code = Column(String, nullable=True)
    color = Column(String, default="#10B981", nullable=False)

    institution = relationship("Institution", back_populates="teachers")
    activities = relationship("ActivityTeacher", back_populates="teacher", cascade="all, delete-orphan")
