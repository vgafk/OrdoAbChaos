from typing import List, Union
from loguru import logger

from sqlalchemy import select, insert

from groups.types import Group
from students.types import StudentGetInput, Student, NewStudentInput

from sql import get_session
from sql import sql_models


async def get_students(where: Union[StudentGetInput | None] = None) -> List[Student]:
    stmt = select(sql_models.Students)
    if where:
        stmt = stmt.where(sql_models.Students.id == where.id) if where.id else stmt
        stmt = stmt.where(sql_models.Students.surname == where.surname) if where.surname else stmt
        stmt = stmt.where(sql_models.Students.name == where.name) if where.name else stmt
        stmt = stmt.where(sql_models.Students.middle_name == where.middle_name) if where.middle_name else stmt
        stmt = stmt.join(sql_models.StudentGroup).where(sql_models.StudentGroup.group_id == where.group_id)\
            if where.group_id else stmt
    logger.debug(stmt)
    async with get_session() as session:
        students_source = (await session.execute(stmt)).all()
        return [Student.from_instance(student[0]) for student in students_source]


async def get_student_for_group(root: Group, student_id: Union[int, None] = None) -> List[Student]:
    logger.debug(student_id)
    stmt = select(sql_models.Students).join(sql_models.StudentGroup).where(sql_models.StudentGroup.group_id == root.id)
    logger.info(f'Запрошена группа c id: {root.id}')
    if student_id:
        stmt = stmt.where(sql_models.Students.id == student_id)
    logger.debug(stmt)
    async with get_session() as session:
        students_source = (await session.execute(stmt)).all()
        return [Student.from_instance(student[0]) for student in students_source]


async def get_student_for_subgroup(root) -> List[Student]:
    stmt = select(sql_models.Students).join(sql_models.StudentSubgroups)\
        .where(sql_models.StudentSubgroups.subgroup_id == root.id)
    async with get_session() as session:
        students_source = (await session.execute(stmt)).all()
        return [Student.from_instance(student[0]) for student in students_source]