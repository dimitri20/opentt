from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.solve_job import SolveJob
from app.schemas.solve_job import SolveJobCreate
from app.services.base import BaseService
from pydantic import BaseModel


class SolveJobUpdate(BaseModel):
    """Internal schema for updating solve job status"""

    status: Optional[str] = None
    solution: Optional[List[dict]] = None
    statistics: Optional[dict] = None
    error_message: Optional[str] = None
    objective_value: Optional[float] = None
    solve_time: Optional[float] = None


class SolveJobService(BaseService[SolveJob, SolveJobCreate, SolveJobUpdate]):
    def __init__(self):
        super().__init__(SolveJob)

    async def get_latest_by_institution(
        self, db: AsyncSession, institution_id: int, limit: int = 10
    ) -> List[SolveJob]:
        """Get latest solve jobs for an institution"""
        result = await db.execute(
            select(SolveJob)
            .where(SolveJob.institution_id == institution_id)
            .order_by(SolveJob.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_latest_completed(
        self, db: AsyncSession, institution_id: int
    ) -> Optional[SolveJob]:
        """Get the most recent completed solve job for an institution"""
        result = await db.execute(
            select(SolveJob)
            .where(SolveJob.institution_id == institution_id)
            .where(SolveJob.status == "completed")
            .order_by(SolveJob.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def update_status(
        self,
        db: AsyncSession,
        *,
        job_id: int,
        status: str,
        solution: Optional[List[dict]] = None,
        statistics: Optional[dict] = None,
        error_message: Optional[str] = None,
        objective_value: Optional[float] = None,
        solve_time: Optional[float] = None,
    ) -> Optional[SolveJob]:
        """Update solve job status and results"""
        job = await self.get_by_id(db, job_id)
        if not job:
            return None

        job.status = status
        if solution is not None:
            job.solution = solution
        if statistics is not None:
            job.statistics = statistics
        if error_message is not None:
            job.error_message = error_message
        if objective_value is not None:
            job.objective_value = objective_value
        if solve_time is not None:
            job.solve_time = solve_time

        await db.commit()
        await db.refresh(job)
        return job


# Service instance
solve_job_service = SolveJobService()
