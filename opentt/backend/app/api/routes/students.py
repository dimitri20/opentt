from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db
from app.services.resource_service import (
    student_year_service,
    student_group_service,
    student_subgroup_service,
)
from app.schemas.student import (
    StudentYearCreate,
    StudentYearUpdate,
    StudentYearRead,
    StudentYearWithGroups,
    StudentGroupCreate,
    StudentGroupUpdate,
    StudentGroupRead,
    StudentGroupWithSubgroups,
    StudentSubgroupCreate,
    StudentSubgroupUpdate,
    StudentSubgroupRead,
)

router = APIRouter()


# Student Year endpoints
@router.post("/{institution_id}/student-years", response_model=StudentYearRead, status_code=status.HTTP_201_CREATED)
async def create_student_year(
    institution_id: int, year: StudentYearCreate, db: AsyncSession = Depends(get_db)
):
    """Create a new student year"""
    return await student_year_service.create(db, obj_in=year, institution_id=institution_id)


@router.get("/{institution_id}/student-years", response_model=List[StudentYearWithGroups])
async def list_student_years(
    institution_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """List student years with groups for an institution"""
    return await student_year_service.get_multi(
        db, skip=skip, limit=limit, filters={"institution_id": institution_id},
        load_relationships=["groups"]
    )


@router.get("/{institution_id}/student-years/{year_id}", response_model=StudentYearWithGroups)
async def get_student_year(
    institution_id: int, year_id: int, db: AsyncSession = Depends(get_db)
):
    """Get student year by ID with groups and subgroups"""
    year = await student_year_service.get_with_groups(db, year_id)
    if not year or year.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Student year not found")
    return year


@router.put("/{institution_id}/student-years/{year_id}", response_model=StudentYearRead)
async def update_student_year(
    institution_id: int,
    year_id: int,
    year: StudentYearUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update student year"""
    updated = await student_year_service.update(db, id=year_id, obj_in=year)
    if not updated or updated.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Student year not found")
    return updated


@router.delete("/{institution_id}/student-years/{year_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_year(
    institution_id: int, year_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete student year"""
    deleted = await student_year_service.delete(db, id=year_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student year not found")


# Student Group endpoints
@router.post("/{institution_id}/student-years/{year_id}/groups", response_model=StudentGroupRead, status_code=status.HTTP_201_CREATED)
async def create_student_group(
    institution_id: int,
    year_id: int,
    group: StudentGroupCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new student group"""
    # Verify year belongs to institution
    year_obj = await student_year_service.get_by_id(db, year_id)
    if not year_obj or year_obj.institution_id != institution_id:
        raise HTTPException(status_code=404, detail="Student year not found")
    
    return await student_group_service.create(db, obj_in=group, year_id=year_id)


@router.get("/{institution_id}/student-years/{year_id}/groups", response_model=List[StudentGroupWithSubgroups])
async def list_student_groups(
    institution_id: int, year_id: int, db: AsyncSession = Depends(get_db)
):
    """List student groups in a year"""
    return await student_group_service.get_by_year(db, year_id)


@router.put("/{institution_id}/student-years/{year_id}/groups/{group_id}", response_model=StudentGroupRead)
async def update_student_group(
    institution_id: int,
    year_id: int,
    group_id: int,
    group: StudentGroupUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update student group"""
    updated = await student_group_service.update(db, id=group_id, obj_in=group)
    if not updated or updated.year_id != year_id:
        raise HTTPException(status_code=404, detail="Student group not found")
    return updated


@router.delete("/{institution_id}/student-years/{year_id}/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_group(
    institution_id: int, year_id: int, group_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete student group"""
    deleted = await student_group_service.delete(db, id=group_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student group not found")


# Student Subgroup endpoints
@router.post("/{institution_id}/student-groups/{group_id}/subgroups", response_model=StudentSubgroupRead, status_code=status.HTTP_201_CREATED)
async def create_student_subgroup(
    institution_id: int,
    group_id: int,
    subgroup: StudentSubgroupCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new student subgroup"""
    # Verify group exists
    group_obj = await student_group_service.get_by_id(db, group_id)
    if not group_obj:
        raise HTTPException(status_code=404, detail="Student group not found")
    
    return await student_subgroup_service.create(db, obj_in=subgroup, group_id=group_id)


@router.get("/{institution_id}/student-groups/{group_id}/subgroups", response_model=List[StudentSubgroupRead])
async def list_student_subgroups(
    institution_id: int, group_id: int, db: AsyncSession = Depends(get_db)
):
    """List student subgroups in a group"""
    return await student_subgroup_service.get_by_group(db, group_id)


@router.put("/{institution_id}/student-groups/{group_id}/subgroups/{subgroup_id}", response_model=StudentSubgroupRead)
async def update_student_subgroup(
    institution_id: int,
    group_id: int,
    subgroup_id: int,
    subgroup: StudentSubgroupUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update student subgroup"""
    updated = await student_subgroup_service.update(db, id=subgroup_id, obj_in=subgroup)
    if not updated or updated.group_id != group_id:
        raise HTTPException(status_code=404, detail="Student subgroup not found")
    return updated


@router.delete("/{institution_id}/student-groups/{group_id}/subgroups/{subgroup_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_subgroup(
    institution_id: int, group_id: int, subgroup_id: int, db: AsyncSession = Depends(get_db)
):
    """Delete student subgroup"""
    deleted = await student_subgroup_service.delete(db, id=subgroup_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student subgroup not found")
