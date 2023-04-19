from typing import Union, List

from sqlalchemy import select, and_
from .types import Group, GroupGetInput, SubgroupGetInput, Subgroup

from sql import get_session, sql_models


async def get_groups(where: Union[GroupGetInput | None] = None) -> List[Group]:
    stmt = select(sql_models.Group).where(sql_models.Group.delete_date.is_(None))
    schedule_week = 0
    if where:
        stmt = stmt.where(sql_models.Group.id == where.id) if where.id else stmt
        stmt = stmt.where(sql_models.Group.name.contains(where.name)) if where.name else stmt
        schedule_week = where.schedule_week

    async with get_session() as session:
        group_source = (await session.execute(stmt)).all()
        group_list = []
        for group in group_source:
            new_group = Group.from_instance(group[0])
            new_group.schedule_week = schedule_week
            group_list.append(new_group)
        return group_list


async def get_group_for_student(root) -> List[Group]:
    stmt = select(sql_models.Group).join(sql_models.StudentGroup)\
        .where(and_(sql_models.StudentGroup.student_id == root.id, sql_models.StudentGroup.remove_date.is_(None)))
    async with get_session() as session:
        group_source = (await session.execute(stmt)).all()
        return [Group.from_instance(group[0]) for group in group_source]


async def get_subgroups(where: Union[SubgroupGetInput | None] = None) -> List[Subgroup]:
    stmt = select(sql_models.Subgroup)
    if where:
        stmt = stmt.where(sql_models.Subgroup.id == where.id) if where.id else stmt
        stmt = stmt.where(sql_models.Subgroup.name.contains(where.name)) if where.name else stmt

    async with get_session() as session:
        subgroup_source = (await session.execute(stmt)).all()
        return [Subgroup.from_instance(subgroup[0]) for subgroup in subgroup_source]


async def get_subgroup_for_student(root) -> List[Subgroup]:
    stmt = select(sql_models.Subgroup).join(sql_models.StudentSubgroups)\
        .where(sql_models.StudentSubgroups.student_id == root.id)
    async with get_session() as session:
        subgroup_source = (await session.execute(stmt)).all()
        return [Subgroup.from_instance(subgroup[0]) for subgroup in subgroup_source]


async def get_group_for_faculty(root) -> List[Group]:
    stmt = select(sql_models.Group).where(sql_models.Group.faculty_id == root.id).order_by(sql_models.Group.name)
    async with get_session() as session:
        group_source = (await session.execute(stmt)).all()
        return [Group.from_instance(group[0]) for group in group_source]


# async def get_group_for_schedule(root) -> Group:
#     stmt = select(sql_models.Group).where(sql_models.Group.id == root.group_id)
#     async with get_session() as session:
#         group_source = (await session.execute(stmt)).scalar()
#         return Group.from_instance(group_source)
#
#
# async def get_subgroup_for_schedule(root) -> Group:
#     stmt = select(sql_models.Subgroup).where(sql_models.Subgroup.id == root.subgroup_id)
#     async with get_session() as session:
#         group_source = (await session.execute(stmt)).scalar()
#         return Group.from_instance(group_source)
