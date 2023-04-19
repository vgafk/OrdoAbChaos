import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sql import sql_models, get_session
from students.types import NewStudentInput

DATABASE_URL = "sqlite+aiosqlite:///database.db"

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@asynccontextmanager
async def get_session_sqlite() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            yield session


async def import_fuculties():
    async with get_session_sqlite() as session:
        query = text(f'SELECT id, `name` FROM faculties')
        result = (await session.execute(query)).all()

        for record in result:
            stmt = insert(sql_models.Faculty).values(id=record[0], name=record[1], full_name=record[1])

            async with get_session() as mysql_session:
                await mysql_session.execute(stmt)
                await mysql_session.commit()


async def import_educationals_forms():
    async with get_session_sqlite() as session:
        query = text(f'SELECT id, `name` FROM educational_forms')
        result = (await session.execute(query)).all()

        for record in result:
            stmt = insert(sql_models.EducationalForm).values(id=record[0], name=record[1])

            async with get_session() as mysql_session:
                await mysql_session.execute(stmt)
                await mysql_session.commit()


async def import_finance_forms():
    async with get_session_sqlite() as session:
        query = text(f'SELECT id, `name` FROM finance_forms')
        result = (await session.execute(query)).all()

        for record in result:
            stmt = insert(sql_models.FinanceForm).values(id=record[0], name=record[1])

            async with get_session() as mysql_session:
                await mysql_session.execute(stmt)
                await mysql_session.commit()


async def import_groups():
    async with get_session_sqlite() as session:
        query = text(f'SELECT id, `name`, full_name, faculty_id, education_form_id FROM groups')
        result = (await session.execute(query)).all()

        for record in result:
            stmt = insert(sql_models.Group).values(id=record[0], name=record[1], full_name=record[2],
                                                         faculty_id=record[3], educational_form_id=record[4])

            async with get_session() as mysql_session:
                await mysql_session.execute(stmt)
                await mysql_session.commit()


async def import_students():
    async with get_session_sqlite() as session:
        query = text(f'SELECT id, surname, name, middle_name, snils, email, finance_form_id, group_id '
                     f'FROM students ')
        result = (await session.execute(query)).all()

        for record in result:
            print(record)
            stmt = insert(sql_models.Students).values(id=record[0],
                                                      surname=record[1],
                                                      name=record[2],
                                                      middle_name=record[3],
                                                      snils=record[4],
                                                      email=record[5],
                                                      finance_form_id=record[6])
            stmt1 = insert(sql_models.StudentGroup).values(student_id=record[0], group_id=record[7])
            async with get_session() as mysql_session:
                await mysql_session.execute(stmt)
                await mysql_session.execute(stmt1)
                await mysql_session.commit()


if __name__ == "__main__":
    # asyncio.run(import_fuculties())
    # asyncio.run(import_educationals_forms())
    # asyncio.run(import_finance_forms())
    # asyncio.run(import_groups())
    asyncio.run(import_students())
