from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.services.resource_service import building_service, room_service
from app.schemas.building import (
    BuildingCreate,
    BuildingUpdate,
    BuildingRead,
    BuildingWithRooms,
    RoomCreate,
    RoomUpdate,
    RoomRead,
)

router = APIRouter()


# Building endpoints
@router.post("/{institution_id}/buildings", response_model=BuildingRead, status_code=status.HTTP_201_CREATED)
async def create_building(
    institution_id: int, building: BuildingCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new building"""
    return await building_service.create(db, obj_in=building, institution_id=institution_id)


@router.get("/{institution_id}/buildings", response_model=List[BuildingRead])
async def list_buildings(
    institution_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List buildings for an institution"""
    return await building_service.get_multi(
        db, skip=skip, limit=limit, filters={"institution_id": institution_id}
    )


@router.get("/{institution_id}/buildings/{building_id}", response_model=BuildingWithRooms)
async def get_building(
    institution_id: int, building_id: int, db: AsyncSession = Depends(get_db)
):
    """Get building by ID with rooms"""
    building = await building_service.get_with_rooms(db, building_id)
    if not building or building.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.put("/{institution_id}/buildings/{building_id}", response_model=BuildingRead)
async def update_building(
    institution_id: int,
    building_id: int,
    building: BuildingUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update building"""
    updated = await building_service.update(db, id=building_id, obj_in=building)
    if not updated or updated.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Building not found")
    return updated


@router.delete("/{institution_id}/buildings/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(
    institution_id: int, building_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete building"""
    deleted = await building_service.delete(db, id=building_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Building not found")


# Room endpoints
@router.post("/{institution_id}/buildings/{building_id}/rooms", response_model=RoomRead, status_code=status.HTTP_201_CREATED)
async def create_room(
    institution_id: int,
    building_id: int,
    room: RoomCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new room in a building"""
    # Verify building belongs to institution
    building_obj = await building_service.get_by_id(db, building_id)
    if not building_obj or building_obj.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Building not found")
    
    return await room_service.create(db, obj_in=room, building_id=building_id)


@router.get("/{institution_id}/buildings/{building_id}/rooms", response_model=List[RoomRead])
async def list_rooms(
    institution_id: int, building_id: int, db: AsyncSession = Depends(get_db)
):
    """List rooms in a building"""
    return await room_service.get_by_building(db, building_id)


@router.get("/{institution_id}/rooms", response_model=List[RoomRead])
async def list_all_rooms(
    institution_id: int, skip: int = 0, limit: int = 200, db: AsyncSession = Depends(get_db)
):
    """List all rooms for an institution"""
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.models.building import Room, Building
    
    result = await db.execute(
        select(Room)
        .join(Building)
        .where(Building.institution_id == institution_id)
        .options(selectinload(Room.building))
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


@router.put("/{institution_id}/buildings/{building_id}/rooms/{room_id}", response_model=RoomRead)
async def update_room(
    institution_id: int,
    building_id: int,
    room_id: int,
    room: RoomUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update room"""
    updated = await room_service.update(db, id=room_id, obj_in=room)
    if not updated or updated.building_id != building_id:
        raise HTTPException(status_code=404, detail="Room not found")
    return updated


@router.delete("/{institution_id}/buildings/{building_id}/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(
    institution_id: int, building_id: int, room_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete room"""
    deleted = await room_service.delete(db, id=room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Room not found")
