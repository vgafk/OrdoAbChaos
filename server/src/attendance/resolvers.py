from typing import Union, List, Dict

from loguru import logger
from sqlalchemy import select, delete, update, insert

from attendance.types import Attendance, AttendanceListInput  # ,  AttendanceType
from sql import get_session
from sql import sql_models


# async def get_attendace_type(root) -> AttendanceType:
#     stmt = select(sql_models.AttendanceType).where(sql_models.AttendanceType.id == root.attendance_type_id)
#     async with get_session() as session:
#         attendance_type_source = (await session.execute(stmt)).scalar()
#     return AttendanceType.from_instance(attendance_type_source)

#
# async def get_groups_lessons_by_group(root, week_number: int):
#
#     stmt = select(sql_models.Schedule).where(and_(sql_models.Schedule.group_id == root.id,
#                                                   sql_models.Schedule.week_number == week_number))
#     async with get_session() as session:
#         lessons_source = (await session.execute(stmt)).all()
#     return [Lesson.from_instance(lesson[0]) for lesson in lessons_source]


async def get_attendace_by_student(root, week_number: Union[int, None] = None) -> List[Attendance]:
    stmt = select(sql_models.Attendance).where(sql_models.Attendance.student_id == root.id)
    if week_number:
        stmt.join(sql_models.Schedule).where(sql_models.Schedule.week_number == week_number)

    async with get_session() as session:
        lessons_source = (await session.execute(stmt)).all()
    return [Attendance.from_instance(lesson[0]) for lesson in lessons_source]


async def delete_attendance(ids: List[int]) -> None:
    stmt = delete(sql_models.Attendance).where(sql_models.Attendance.id.in_(ids))
    async with get_session() as session:
        await session.execute(stmt)
        await session.commit()


async def update_attendance(alist: List[AttendanceListInput]) -> None:
    logger.info(alist)
    for attendance in alist:
        stmt = update(sql_models.Attendance).where(sql_models.Attendance.id.in_(attendance.ids))\
            .values(attendance_type_id=attendance.reason)
        async with get_session() as session:
            await session.execute(stmt)
            await session.commit()


async def add_attendance(alist: List[AttendanceListInput]) -> None:
    logger.info(alist)
    for attendance in alist:
        stmt = insert(sql_models.Attendance).values(student_id=attendance.student_id, schedule_id=attendance.lesson_id,
                                                    attendance_type_id=attendance.reason)
        async with get_session() as session:
            await session.execute(stmt)
            await session.commit()
