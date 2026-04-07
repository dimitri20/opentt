from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


# Solution assignment schema
class Assignment(BaseModel):
    activity_id: int
    activity_name: str
    day_id: int
    day_name: str
    period_id: int
    period_name: str
    room_id: Optional[int] = None
    room_name: Optional[str] = None


# SolveJob schemas
class SolveJobCreate(BaseModel):
    time_limit_seconds: int = Field(default=300, ge=10, le=3600)


class SolveJobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    status: str  # pending, running, completed, failed
    time_limit_seconds: int
    solution: Optional[List[Dict[str, Any]]] = None
    statistics: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    objective_value: Optional[float] = None
    solve_time: Optional[float] = None
    created_at: datetime
    updated_at: datetime


# Progress update schema (sent via WebSocket/SSE)
class SolveProgress(BaseModel):
    job_id: int
    status: str
    solutions_found: int = 0
    current_objective: Optional[float] = None
    best_objective: Optional[float] = None
    time_elapsed: float = 0.0
    message: Optional[str] = None
