from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.services.resource_service import teacher_service
from app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherRead

router = APIRouter()


@router.post("/{institution_id}/teachers", response_model=TeacherRead, status_code=status.HTTP_201_CREATED)
async def create_teacher(
    institution_id: int, teacher: TeacherCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new teacher"""
    return await teacher_service.create(db, obj_in=teacher, institution_id=institution_id)


@router.get("/{institution_id}/teachers", response_model=List[TeacherRead])
async def list_teachers(
    institution_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List teachers for an institution"""
    return await teacher_service.get_multi(
        db, skip=skip, limit=limit, filters={"institution_id": institution_id}
    )


@router.get("/{institution_id}/teachers/{teacher_id}", response_model=TeacherRead)
async def get_teacher(
    institution_id: int, teacher_id: int, db: AsyncSession = Depends(get_db)
):
    """Get teacher by ID"""
    teacher = await teacher_service.get_by_id(db, teacher_id)
    if not teacher or teacher.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@router.put("/{institution_id}/teachers/{teacher_id}", response_model=TeacherRead)
async def update_teacher(
    institution_id: int,
    teacher_id: int,
    teacher: TeacherUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update teacher"""
    updated = await teacher_service.update(db, id=teacher_id, obj_in=teacher)
    if not updated or updated.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return updated


@router.delete("/{institution_id}/teachers/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(
    institution_id: int, teacher_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete teacher"""
    deleted = await teacher_service.delete(db, id=teacher_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Teacher not found")
