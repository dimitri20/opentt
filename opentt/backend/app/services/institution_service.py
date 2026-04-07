from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.institution import Institution, AcademicYear, DayOfWeek, Period
from app.schemas.institution import (
    InstitutionCreate,
    InstitutionUpdate,
    AcademicYearCreate,
    AcademicYearUpdate,
    DayOfWeekCreate,
    DayOfWeekUpdate,
    PeriodCreate,
    PeriodUpdate,
)
from app.services.base import BaseService


class InstitutionService(BaseService[Institution, InstitutionCreate, InstitutionUpdate]):
    def __init__(self):
        super().__init__(Institution)

    async def get_by_slug(self, db: AsyncSession, slug: str) -> Optional[Institution]:
        """Get institution by slug"""
        result = await db.execute(select(Institution).where(Institution.slug == slug))
        return result.scalar_one_or_none()

    async def get_with_setup(self, db: AsyncSession, institution_id: int) -> Optional[Institution]:
        """Get institution with days, periods, and academic years"""
        result = await db.execute(
            select(Institution)
            .where(Institution.id == institution_id)
            .options(
                selectinload(Institution.days_of_week),
                selectinload(Institution.periods),
                selectinload(Institution.academic_years),
            )
        )
        return result.scalar_one_or_none()


class AcademicYearService(BaseService[AcademicYear, AcademicYearCreate, AcademicYearUpdate]):
    def __init__(self):
        super().__init__(AcademicYear)


class DayOfWeekService(BaseService[DayOfWeek, DayOfWeekCreate, DayOfWeekUpdate]):
    def __init__(self):
        super().__init__(DayOfWeek)

    async def get_by_institution(
        self, db: AsyncSession, institution_id: int, active_only: bool = True
    ):
        """Get all days for an institution, optionally filtered by active status"""
        from sqlalchemy import and_
        
        query = select(DayOfWeek).where(DayOfWeek.institution_id == institution_id)
        if active_only:
            query = query.where(DayOfWeek.is_active == True)
        query = query.order_by(DayOfWeek.order)
        
        result = await db.execute(query)
        return list(result.scalars().all())


class PeriodService(BaseService[Period, PeriodCreate, PeriodUpdate]):
    def __init__(self):
        super().__init__(Period)

    async def get_by_institution(self, db: AsyncSession, institution_id: int):
        """Get all periods for an institution ordered by order"""
        query = (
            select(Period)
            .where(Period.institution_id == institution_id)
            .order_by(Period.order)
        )
        result = await db.execute(query)
        return list(result.scalars().all())


# Service instances
institution_service = InstitutionService()
academic_year_service = AcademicYearService()
day_of_week_service = DayOfWeekService()
period_service = PeriodService()
