from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.services.institution_service import (
    institution_service,
    academic_year_service,
    day_of_week_service,
    period_service,
)
from app.schemas.institution import (
    InstitutionCreate,
    InstitutionUpdate,
    InstitutionRead,
    AcademicYearCreate,
    AcademicYearUpdate,
    AcademicYearRead,
    DayOfWeekCreate,
    DayOfWeekUpdate,
    DayOfWeekRead,
    PeriodCreate,
    PeriodUpdate,
    PeriodRead,
)

router = APIRouter()


# Institution endpoints
@router.post("/", response_model=InstitutionRead, status_code=status.HTTP_201_CREATED)
async def create_institution(
    institution: InstitutionCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new institution"""
    # Check if slug already exists
    existing = await institution_service.get_by_slug(db, institution.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Institution with slug '{institution.slug}' already exists",
        )
    return await institution_service.create(db, obj_in=institution)


@router.get("/", response_model=List[InstitutionRead])
async def list_institutions(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List all institutions"""
    return await institution_service.get_multi(db, skip=skip, limit=limit)


@router.get("/{institution_id}", response_model=InstitutionRead)
async def get_institution(institution_id: int, db: AsyncSession = Depends(get_db)):
    """Get institution by ID"""
    institution = await institution_service.get_by_id(db, institution_id)
    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return institution


@router.put("/{institution_id}", response_model=InstitutionRead)
async def update_institution(
    institution_id: int, institution: InstitutionUpdate, db: AsyncSession = Depends(get_db)
):
    """Update institution"""
    updated = await institution_service.update(db, id=institution_id, obj_in=institution)
    if not updated:
        raise HTTPException(status_code=404, detail="Institution not found")
    return updated


@router.delete("/{institution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_institution(institution_id: int, db: AsyncSession = Depends(get_db)):
    """Delete institution"""
    deleted = await institution_service.delete(db, id=institution_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Institution not found")


# Academic Year endpoints
@router.post(
    "/{institution_id}/academic-years",
    response_model=AcademicYearRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_academic_year(
    institution_id: int, academic_year: AcademicYearCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new academic year"""
    return await academic_year_service.create(
        db, obj_in=academic_year, institution_id=institution_id
    )


@router.get("/{institution_id}/academic-years", response_model=List[AcademicYearRead])
async def list_academic_years(
    institution_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List academic years for an institution"""
    return await academic_year_service.get_multi(
        db, skip=skip, limit=limit, filters={"institution_id": institution_id}
    )


@router.put(
    "/{institution_id}/academic-years/{year_id}", response_model=AcademicYearRead
)
async def update_academic_year(
    institution_id: int,
    year_id: int,
    academic_year: AcademicYearUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update academic year"""
    updated = await academic_year_service.update(db, id=year_id, obj_in=academic_year)
    if not updated:
        raise HTTPException(status_code=404, detail="Academic year not found")
    return updated


@router.delete(
    "/{institution_id}/academic-years/{year_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_academic_year(
    institution_id: int, year_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete academic year"""
    deleted = await academic_year_service.delete(db, id=year_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Academic year not found")


# Day of Week endpoints
@router.post(
    "/{institution_id}/days",
    response_model=DayOfWeekRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_day(
    institution_id: int, day: DayOfWeekCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new day of week"""
    return await day_of_week_service.create(db, obj_in=day, institution_id=institution_id)


@router.get("/{institution_id}/days", response_model=List[DayOfWeekRead])
async def list_days(institution_id: int, db: AsyncSession = Depends(get_db)):
    """List days for an institution"""
    return await day_of_week_service.get_by_institution(db, institution_id, active_only=False)


@router.put("/{institution_id}/days/{day_id}", response_model=DayOfWeekRead)
async def update_day(
    institution_id: int,
    day_id: int,
    day: DayOfWeekUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update day of week"""
    updated = await day_of_week_service.update(db, id=day_id, obj_in=day)
    if not updated:
        raise HTTPException(status_code=404, detail="Day not found")
    return updated


@router.delete("/{institution_id}/days/{day_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_day(
    institution_id: int, day_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete day of week"""
    deleted = await day_of_week_service.delete(db, id=day_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Day not found")


# Period endpoints
@router.post(
    "/{institution_id}/periods",
    response_model=PeriodRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_period(
    institution_id: int, period: PeriodCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new period"""
    return await period_service.create(db, obj_in=period, institution_id=institution_id)


@router.get("/{institution_id}/periods", response_model=List[PeriodRead])
async def list_periods(institution_id: int, db: AsyncSession = Depends(get_db)):
    """List periods for an institution"""
    return await period_service.get_by_institution(db, institution_id)


@router.put("/{institution_id}/periods/{period_id}", response_model=PeriodRead)
async def update_period(
    institution_id: int,
    period_id: int,
    period: PeriodUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update period"""
    updated = await period_service.update(db, id=period_id, obj_in=period)
    if not updated:
        raise HTTPException(status_code=404, detail="Period not found")
    return updated


@router.delete("/{institution_id}/periods/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_period(
    institution_id: int, period_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete period"""
    deleted = await period_service.delete(db, id=period_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Period not found")
