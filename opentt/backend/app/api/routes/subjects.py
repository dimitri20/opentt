from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.services.resource_service import subject_service
from app.schemas.subject import SubjectCreate, SubjectUpdate, SubjectRead

router = APIRouter()


@router.post("/{institution_id}/subjects", response_model=SubjectRead, status_code=status.HTTP_201_CREATED)
async def create_subject(
    institution_id: int, subject: SubjectCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new subject"""
    return await subject_service.create(db, obj_in=subject, institution_id=institution_id)


@router.get("/{institution_id}/subjects", response_model=List[SubjectRead])
async def list_subjects(
    institution_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List subjects for an institution"""
    return await subject_service.get_multi(
        db, skip=skip, limit=limit, filters={"institution_id": institution_id}
    )


@router.get("/{institution_id}/subjects/{subject_id}", response_model=SubjectRead)
async def get_subject(
    institution_id: int, subject_id: int, db: AsyncSession = Depends(get_db)
):
    """Get subject by ID"""
    subject = await subject_service.get_by_id(db, subject_id)
    if not subject or subject.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@router.put("/{institution_id}/subjects/{subject_id}", response_model=SubjectRead)
async def update_subject(
    institution_id: int,
    subject_id: int,
    subject: SubjectUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update subject"""
    updated = await subject_service.update(db, id=subject_id, obj_in=subject)
    if not updated or updated.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Subject not found")
    return updated


@router.delete("/{institution_id}/subjects/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(
    institution_id: int, subject_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete subject"""
    deleted = await subject_service.delete(db, id=subject_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Subject not found")
