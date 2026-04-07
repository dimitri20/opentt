from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.activity import (
    Activity,
    ActivityTeacher,
    ActivityStudentGroup,
    ActivityStudentSubgroup,
    ActivityPreferredRoom,
)
from app.schemas.activity import ActivityCreate, ActivityUpdate
from app.services.base import BaseService


class ActivityService(BaseService[Activity, ActivityCreate, ActivityUpdate]):
    def __init__(self):
        super().__init__(Activity)

    async def create_with_relations(
        self, db: AsyncSession, *, obj_in: ActivityCreate, institution_id: int
    ) -> Activity:
        """Create activity with all relationships in a single transaction"""
        # Extract relationship IDs
        teacher_ids = obj_in.teacher_ids or []
        group_ids = obj_in.group_ids or []
        subgroup_ids = obj_in.subgroup_ids or []
        preferred_room_ids = obj_in.preferred_room_ids or []
        tag_ids = obj_in.tag_ids or []

        # Create activity
        activity_data = obj_in.model_dump(
            exclude={"teacher_ids", "group_ids", "subgroup_ids", "preferred_room_ids", "tag_ids"}
        )
        activity = Activity(**activity_data, institution_id=institution_id)
        db.add(activity)
        await db.flush()  # Get activity.id without committing

        # Add teachers
        for teacher_id in teacher_ids:
            activity_teacher = ActivityTeacher(activity_id=activity.id, teacher_id=teacher_id)
            db.add(activity_teacher)

        # Add groups
        for group_id in group_ids:
            activity_group = ActivityStudentGroup(activity_id=activity.id, group_id=group_id)
            db.add(activity_group)

        # Add subgroups
        for subgroup_id in subgroup_ids:
            activity_subgroup = ActivityStudentSubgroup(
                activity_id=activity.id, subgroup_id=subgroup_id
            )
            db.add(activity_subgroup)

        # Add preferred rooms
        for idx, room_id in enumerate(preferred_room_ids):
            activity_room = ActivityPreferredRoom(
                activity_id=activity.id, room_id=room_id, priority=idx + 1
            )
            db.add(activity_room)

        await db.commit()
        await db.refresh(activity)

        # Load relationships
        result = await db.execute(
            select(Activity)
            .where(Activity.id == activity.id)
            .options(
                selectinload(Activity.subject),
                selectinload(Activity.teachers),
                selectinload(Activity.student_groups),
                selectinload(Activity.student_subgroups),
                selectinload(Activity.preferred_rooms),
                selectinload(Activity.tags),
            )
        )
        return result.scalar_one()

    async def update_with_relations(
        self, db: AsyncSession, *, id: int, obj_in: ActivityUpdate
    ) -> Optional[Activity]:
        """Update activity and its relationships"""
        activity = await self.get_by_id(db, id)
        if not activity:
            return None

        # Update basic fields
        update_data = obj_in.model_dump(
            exclude_unset=True,
            exclude={"teacher_ids", "group_ids", "subgroup_ids", "preferred_room_ids", "tag_ids"},
        )
        for field, value in update_data.items():
            setattr(activity, field, value)

        # Update teachers if provided
        if obj_in.teacher_ids is not None:
            # Delete existing
            await db.execute(
                select(ActivityTeacher).where(ActivityTeacher.activity_id == id)
            )
            await db.execute(
                ActivityTeacher.__table__.delete().where(ActivityTeacher.activity_id == id)
            )
            # Add new
            for teacher_id in obj_in.teacher_ids:
                activity_teacher = ActivityTeacher(activity_id=id, teacher_id=teacher_id)
                db.add(activity_teacher)

        # Update groups if provided
        if obj_in.group_ids is not None:
            await db.execute(
                ActivityStudentGroup.__table__.delete().where(
                    ActivityStudentGroup.activity_id == id
                )
            )
            for group_id in obj_in.group_ids:
                activity_group = ActivityStudentGroup(activity_id=id, group_id=group_id)
                db.add(activity_group)

        # Update subgroups if provided
        if obj_in.subgroup_ids is not None:
            await db.execute(
                ActivityStudentSubgroup.__table__.delete().where(
                    ActivityStudentSubgroup.activity_id == id
                )
            )
            for subgroup_id in obj_in.subgroup_ids:
                activity_subgroup = ActivityStudentSubgroup(
                    activity_id=id, subgroup_id=subgroup_id
                )
                db.add(activity_subgroup)

        # Update preferred rooms if provided
        if obj_in.preferred_room_ids is not None:
            await db.execute(
                ActivityPreferredRoom.__table__.delete().where(
                    ActivityPreferredRoom.activity_id == id
                )
            )
            for idx, room_id in enumerate(obj_in.preferred_room_ids):
                activity_room = ActivityPreferredRoom(
                    activity_id=id, room_id=room_id, priority=idx + 1
                )
                db.add(activity_room)

        await db.commit()
        await db.refresh(activity)

        # Load relationships
        result = await db.execute(
            select(Activity)
            .where(Activity.id == id)
            .options(
                selectinload(Activity.subject),
                selectinload(Activity.teachers),
                selectinload(Activity.student_groups),
                selectinload(Activity.student_subgroups),
                selectinload(Activity.preferred_rooms),
                selectinload(Activity.tags),
            )
        )
        return result.scalar_one()

    async def get_with_relations(self, db: AsyncSession, id: int) -> Optional[Activity]:
        """Get activity with all relationships loaded"""
        result = await db.execute(
            select(Activity)
            .where(Activity.id == id)
            .options(
                selectinload(Activity.subject),
                selectinload(Activity.teachers).selectinload(ActivityTeacher.teacher),
                selectinload(Activity.student_groups).selectinload(
                    ActivityStudentGroup.group
                ),
                selectinload(Activity.student_subgroups).selectinload(
                    ActivityStudentSubgroup.subgroup
                ),
                selectinload(Activity.preferred_rooms).selectinload(
                    ActivityPreferredRoom.room
                ),
                selectinload(Activity.tags),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_institution(
        self, db: AsyncSession, institution_id: int
    ) -> List[Activity]:
        """Get all activities for an institution with relationships"""
        result = await db.execute(
            select(Activity)
            .where(Activity.institution_id == institution_id)
            .options(
                selectinload(Activity.subject),
                selectinload(Activity.teachers).selectinload(ActivityTeacher.teacher),
                selectinload(Activity.student_groups).selectinload(
                    ActivityStudentGroup.group
                ),
            )
        )
        return list(result.scalars().all())


# Service instance
activity_service = ActivityService()
