from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.services.solve_job_service import solve_job_service
from app.schemas.solve_job import SolveJobCreate, SolveJobRead
from app.tasks.solve_tasks import solve_timetable

router = APIRouter()


@router.post("/{institution_id}/solve", response_model=SolveJobRead, status_code=status.HTTP_201_CREATED)
async def start_solve(
    institution_id: int,
    solve_request: SolveJobCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Start a new timetable solving job"""
    # Create solve job record
    job = await solve_job_service.create(
        db,
        obj_in=solve_request,
        institution_id=institution_id,
    )
    
    # Start async solving task
    solve_timetable.delay(
        job_id=job.id,
        institution_id=institution_id,
        time_limit=solve_request.time_limit_seconds,
    )
    
    return job


@router.get("/{institution_id}/solve-jobs", response_model=List[SolveJobRead])
async def list_solve_jobs(
    institution_id: int,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """List recent solve jobs for an institution"""
    return await solve_job_service.get_latest_by_institution(
        db, institution_id=institution_id, limit=limit
    )


@router.get("/{institution_id}/solve-jobs/{job_id}", response_model=SolveJobRead)
async def get_solve_job(
    institution_id: int,
    job_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get solve job by ID"""
    job = await solve_job_service.get_by_id(db, job_id)
    if not job or job.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Solve job not found")
    return job


@router.get("/{institution_id}/solve-jobs/latest/completed", response_model=SolveJobRead)
async def get_latest_completed_solution(
    institution_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get the latest completed solution for an institution"""
    job = await solve_job_service.get_latest_completed(db, institution_id=institution_id)
    if not job:
        raise HTTPException(status_code=404, detail="No completed solution found")
    return job
