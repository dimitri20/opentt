import asyncio
from celery import Task
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.solver.data_loader import load_institution_data
from app.solver.timetable_solver import TimetableSolver
from app.services.solve_job_service import solve_job_service


class DatabaseTask(Task):
    """Base task that handles database sessions"""
    _session = None

    def after_return(self, *args, **kwargs):
        if self._session is not None:
            asyncio.run(self._session.close())


@celery_app.task(bind=True, base=DatabaseTask, name="solve_timetable")
def solve_timetable(self, job_id: int, institution_id: int, time_limit: int = 300):
    """Solve timetable problem asynchronously"""
    
    async def _solve():
        async with AsyncSessionLocal() as db:
            try:
                # Update job status to running
                await solve_job_service.update_status(
                    db, job_id=job_id, status="running"
                )
                
                # Load data
                print(f"📊 Loading data for institution {institution_id}...")
                data = await load_institution_data(institution_id, db)
                
                # Build and solve model
                solver = TimetableSolver(data)
                solver.build_model()
                
                result = solver.solve(time_limit_seconds=time_limit)
                
                # Update job with results
                if result.status in ("OPTIMAL", "FEASIBLE"):
                    await solve_job_service.update_status(
                        db,
                        job_id=job_id,
                        status="completed",
                        solution=result.assignments,
                        statistics=result.statistics,
                        objective_value=result.objective_value,
                        solve_time=result.solve_time,
                    )
                    print(f"✅ Solution saved for job {job_id}")
                else:
                    await solve_job_service.update_status(
                        db,
                        job_id=job_id,
                        status="failed",
                        error_message=f"No solution found: {result.status}",
                        statistics=result.statistics,
                        solve_time=result.solve_time,
                    )
                    print(f"❌ Failed to find solution for job {job_id}")
                
                return {
                    "status": result.status,
                    "assignments_count": len(result.assignments),
                    "solve_time": result.solve_time,
                }
                
            except Exception as e:
                print(f"❌ Error solving timetable: {str(e)}")
                import traceback
                traceback.print_exc()
                
                # Update job with error
                await solve_job_service.update_status(
                    db,
                    job_id=job_id,
                    status="failed",
                    error_message=str(e),
                )
                raise
    
    return asyncio.run(_solve())
