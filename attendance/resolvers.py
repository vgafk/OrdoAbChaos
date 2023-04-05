from typing import Union, List, TYPE_CHECKING

from sqlalchemy import select

from attendance.types import Attendance #,  AttendanceType
from sql import sql_models, get_session


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
