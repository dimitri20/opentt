from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class SolveJob(BaseModel):
    __tablename__ = "solve_jobs"

    institution_id = Column(Integer, ForeignKey("institutions.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="pending", nullable=False)
    time_limit_seconds = Column(Integer, default=300, nullable=False)
    solution = Column(JSON, nullable=True)
    statistics = Column(JSON, nullable=True)
    error_message = Column(String, nullable=True)
    objective_value = Column(Float, nullable=True)
    solve_time = Column(Float, nullable=True)

    institution = relationship("Institution", back_populates="solve_jobs")
