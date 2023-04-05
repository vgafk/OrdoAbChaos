from typing import Union, List
from loguru import logger
import strawberry
from sqlalchemy import select

from .types import FacultiesGetInput, Faculty
from sql import sql_models, get_session


async def get_faculties(where: Union[FacultiesGetInput | None] = None) -> List[Faculty]:
    logger.debug(where)
    stmt = select(sql_models.Faculty).order_by(sql_models.Faculty.name)
    if where:
        stmt = stmt.where(sql_models.Faculty.id == where.id) if where.id else stmt
        stmt = stmt.where(sql_models.Faculty.name.contains(where.name)) if where.name else stmt

    async with get_session() as session:
        faculties_source = (await session.execute(stmt)).all()
        return [Faculty.from_instance(group[0]) for group in faculties_source]
#
#
# async def get_group_for_student(root) -> SelectGroupResponse:
#     stmt = select(sql_models.Group).join(sql_models.StudentGroup)\
#         .where(and_(sql_models.StudentGroup.student_id == root.id, sql_models.StudentGroup.remove_date.is_(None)))
#     async with get_session() as session:
#         group_source = (await session.execute(stmt)).all()
#         return [Group.from_instance(group[0]) for group in group_source]
#
#
# async def get_subgroups(params: Union[SubgroupGetInput | None] = None) -> SelectSubgroupResponse:
#     stmt = select(sql_models.Subgroup)
#     if params:
#         stmt = stmt.where(sql_models.Subgroup.id == params.id) if params.id else stmt
#         stmt = stmt.where(sql_models.Subgroup.name.contains(params.name)) if params.name else stmt
#
#     async with get_session() as session:
#         subgroup_source = (await session.execute(stmt)).all()
#
#         if not subgroup_source:
#             return [SubgroupNotFound]
#
#         return [Subgroup.from_instance(subgroup[0]) for subgroup in subgroup_source]
#
#
# async def get_subgroup_for_student(root) -> SelectSubgroupResponse:
#     stmt = select(sql_models.Subgroup).join(sql_models.StudentSubgroups)\
#         .where(sql_models.StudentSubgroups.student_id == root.id)
#     async with get_session() as session:
#         subgroup_source = (await session.execute(stmt)).all()
#         return [Subgroup.from_instance(subgroup[0]) for subgroup in subgroup_source]
#
#
#
#
