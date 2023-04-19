import strawberry

from attendance.resolvers import delete_attendance, update_attendance, add_attendance
from attendance.types import SaveDataInput
from schedule.resolvers import create_week_schedule
from schedule.types import ScheduleGetInput


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_week_schedule(self, params: ScheduleGetInput) -> None:
        await create_week_schedule(params)

    @strawberry.mutation
    async def save_absents(self, data: SaveDataInput) -> None:
        await delete_attendance(data.deleted)
        await update_attendance(data.updated)
        await add_attendance(data.added)
