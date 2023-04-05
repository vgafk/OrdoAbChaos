import strawberry

from schedule.resolvers import create_week_schedule
from schedule.types import ScheduleGetInput


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_week_schedule(self, params: ScheduleGetInput) -> None:
        await create_week_schedule(params)
