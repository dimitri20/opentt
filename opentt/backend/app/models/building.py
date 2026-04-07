from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Building(BaseModel):
    __tablename__ = "buildings"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    address = Column(String, nullable=True)

    institution = relationship("Institution", back_populates="buildings")
    rooms = relationship("Room", back_populates="building", cascade="all, delete-orphan", lazy="selectin")


class Room(BaseModel):
    __tablename__ = "rooms"

    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)
    capacity = Column(Integer, default=0, nullable=False)
    room_type = Column(String, nullable=True)

    building = relationship("Building", back_populates="rooms")
    preferred_activities = relationship("ActivityPreferredRoom", back_populates="room", cascade="all, delete-orphan")
