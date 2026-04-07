from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class RoomNotAvailable(BaseModel):
    __tablename__ = "constraint_room_not_available"

    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    day_id = Column(Integer, ForeignKey("days_of_week.id", ondelete="CASCADE"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.id", ondelete="CASCADE"), nullable=False)
    is_hard = Column(Boolean, default=True, nullable=False)
    weight = Column(Integer, default=100, nullable=False)

    room = relationship("Room")
    day = relationship("DayOfWeek")
    period = relationship("Period")
