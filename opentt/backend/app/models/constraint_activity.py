from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ActivityPreferredStartingTime(BaseModel):
    __tablename__ = "constraint_activity_preferred_starting_time"

    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    day_id = Column(Integer, ForeignKey("days_of_week.id", ondelete="CASCADE"), nullable=False)
    period_id = Column(Integer, ForeignKey("periods.id", ondelete="CASCADE"), nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    activity = relationship("Activity")
    day = relationship("DayOfWeek")
    period = relationship("Period")


class ActivityPreferredStartingDay(BaseModel):
    __tablename__ = "constraint_activity_preferred_starting_day"

    activity_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    day_id = Column(Integer, ForeignKey("days_of_week.id", ondelete="CASCADE"), nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    activity = relationship("Activity")
    day = relationship("DayOfWeek")


class ActivitiesNotOnSameDay(BaseModel):
    __tablename__ = "constraint_activities_not_on_same_day"

    activity1_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    activity2_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    activity1 = relationship("Activity", foreign_keys=[activity1_id])
    activity2 = relationship("Activity", foreign_keys=[activity2_id])


class ActivitiesConsecutive(BaseModel):
    __tablename__ = "constraint_activities_consecutive"

    activity1_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    activity2_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    is_hard = Column(Boolean, default=False, nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    activity1 = relationship("Activity", foreign_keys=[activity1_id])
    activity2 = relationship("Activity", foreign_keys=[activity2_id])


class ActivitiesSameStartingTime(BaseModel):
    __tablename__ = "constraint_activities_same_starting_time"

    activity1_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    activity2_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    is_hard = Column(Boolean, default=False, nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    activity1 = relationship("Activity", foreign_keys=[activity1_id])
    activity2 = relationship("Activity", foreign_keys=[activity2_id])


class ActivitiesSameStartingDay(BaseModel):
    __tablename__ = "constraint_activities_same_starting_day"

    activity1_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    activity2_id = Column(Integer, ForeignKey("activities.id", ondelete="CASCADE"), nullable=False)
    is_hard = Column(Boolean, default=False, nullable=False)
    weight = Column(Integer, default=10, nullable=False)

    activity1 = relationship("Activity", foreign_keys=[activity1_id])
    activity2 = relationship("Activity", foreign_keys=[activity2_id])
