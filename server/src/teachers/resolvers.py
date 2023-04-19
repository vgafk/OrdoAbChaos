from sqlalchemy import select


from sql import get_session, sql_models
from teachers.types import SelectTeacherResponse, Teacher, TeacherNotFound


async def get_teacher_for_schedule(root) -> SelectTeacherResponse:
    stmt = select(sql_models.Teacher).outerjoin(sql_models.TeacherSchedule)\
        .where(sql_models.TeacherSchedule.schedule_id == root.id)
    async with get_session() as session:
        teacher_source = (await session.execute(stmt)).scalar()
        if not teacher_source:
            return TeacherNotFound
        return Teacher.from_instance(teacher_source)
