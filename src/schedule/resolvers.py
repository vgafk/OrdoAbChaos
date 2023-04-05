from datetime import date, timedelta
from typing import List

from isoweek import Week
from sqlalchemy import select, and_, insert

from schedule.types import ScheduleGetInput, Lesson

from sql import get_session, sql_models


async def create_week_schedule(root: ScheduleGetInput):  # -> Schedule:
    monday_date = Week(date.today().year, root.week_number).monday()
    for day in range(5):
        current_date = monday_date + timedelta(days=day)
        for number_in_day in range(1, 6):
            lesson_id = await create_lesson_schedule(current_date, number_in_day, root.group_id,
                                                     root.week_number)
            await create_teacher_schedule(1, lesson_id)


async def create_lesson_schedule(current_date: date, number_in_day: int, group_id: int, week_number: int):
    stmt = insert(sql_models.Schedule).values(date=current_date, number_in_day=number_in_day, group_id=group_id,
                                              week_number=week_number, discipline_id=1)
    async with get_session() as session:
        result = (await session.execute(stmt))
        await session.commit()
    return result.lastrowid


async def create_teacher_schedule(teacher_id: int, schedule_id: int):
    stmt = insert(sql_models.TeacherSchedule).values(teacher_id=teacher_id, schedule_id=schedule_id)
    async with get_session() as session:
        result = (await session.execute(stmt))
        await session.commit()
    return result.lastrowid


async def get_lessons_by_id(root) -> Lesson:
    stmt = select(sql_models.Schedule).where(sql_models.Schedule.id == root.lesson_id)
    async with get_session() as session:
        lessons_source = (await session.execute(stmt)).scalar()
    return Lesson.from_instance(lessons_source)


async def get_groups_lessons_by_group(root, week_number: int) -> List[Lesson]:

    stmt = select(sql_models.Schedule).where(and_(sql_models.Schedule.group_id == root.id,
                                                  sql_models.Schedule.week_number == week_number))
    async with get_session() as session:
        lessons_source = (await session.execute(stmt)).all()
    return [Lesson.from_instance(lesson[0]) for lesson in lessons_source]

