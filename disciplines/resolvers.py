from sqlalchemy import select

from sql import sql_models, get_session
from .types import Discipline, SelectDisciplineResponse, DisciplineNotFound


async def get_discipline_for_schedule(root) -> SelectDisciplineResponse:
    stmt = select(sql_models.Discipline).join(sql_models.Schedule).where(sql_models.Schedule.id == root.id)
    async with get_session() as session:
        disciplines_source = (await session.execute(stmt)).scalar()
        if not disciplines_source:
            return DisciplineNotFound
        return Discipline.from_instance(disciplines_source)