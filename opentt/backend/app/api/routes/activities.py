from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.services.activity_service import activity_service
from app.schemas.activity import ActivityCreate, ActivityUpdate, ActivityRead, ActivityWithRelations

router = APIRouter()


@router.post("/{institution_id}/activities", response_model=ActivityWithRelations, status_code=status.HTTP_201_CREATED)
async def create_activity(
    institution_id: int, activity: ActivityCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new activity with relationships"""
    return await activity_service.create_with_relations(
        db, obj_in=activity, institution_id=institution_id
    )


@router.get("/{institution_id}/activities", response_model=List[ActivityWithRelations])
async def list_activities(
    institution_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List activities for an institution"""
    return await activity_service.get_by_institution(db, institution_id)


@router.get("/{institution_id}/activities/{activity_id}", response_model=ActivityWithRelations)
async def get_activity(
    institution_id: int, activity_id: int, db: AsyncSession = Depends(get_db)
):
    """Get activity by ID with all relationships"""
    activity = await activity_service.get_with_relations(db, activity_id)
    if not activity or activity.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@router.put("/{institution_id}/activities/{activity_id}", response_model=ActivityWithRelations)
async def update_activity(
    institution_id: int,
    activity_id: int,
    activity: ActivityUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update activity and its relationships"""
    updated = await activity_service.update_with_relations(db, id=activity_id, obj_in=activity)
    if not updated or updated.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated


@router.delete("/{institution_id}/activities/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    institution_id: int, activity_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete activity"""
    deleted = await activity_service.delete(db, id=activity_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Activity not found")
