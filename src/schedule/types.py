from datetime import datetime
import strawberry

from disciplines.resolvers import get_discipline_for_schedule
from disciplines.types import SelectDisciplineResponse
from sql import Schedule
# from groups.resolvers import get_group_for_schedule, get_subgroup_for_schedule
# from groups.types import Group, Subgroup
from teachers.resolvers import get_teacher_for_schedule
from teachers.types import SelectTeacherResponse


@strawberry.input
class ScheduleGetInput:
    week_number: int
    group_id: int


@strawberry.type
class Lesson:
    id: strawberry.ID
    date: datetime
    number_in_day: int
    week_number: int
    teacher: SelectTeacherResponse = strawberry.field(resolver=get_teacher_for_schedule)
    discipline: SelectDisciplineResponse = strawberry.field(resolver=get_discipline_for_schedule)
    # group_id: int
    # subgroup_id: int
    # group: Group = strawberry.field(resolver=get_group_for_schedule)
    # subgroup: Subgroup = strawberry.field(resolver=get_subgroup_for_schedule)

    @classmethod
    def from_instance(cls, instance: Schedule) -> "Lesson":
        return cls(id=strawberry.ID(instance.id),
                   date=instance.date,
                   number_in_day=instance.number_in_day,
                   week_number=instance.week_number)  #,
                   # group_id=instance.group_id,
                   # subgroup_id=instance.subgroup_id)


# @strawberry.type
# class GroupNotFound:
#     error: str = "Группы не существует"
#
#
# SelectGroupResponse = strawberry.union("SelectGroupResponse",
#                                        (Group,
#                                         GroupNotFound))
#
#
# @strawberry.input
# class SubgroupGetInput:
#     id: Optional[int] = strawberry.UNSET
#     name: Optional[str] = strawberry.UNSET
#
#     def is_empty(self):
#         return not any([self.id, self.name])
#
#
# @strawberry.type
# class Subgroup:
#     id: strawberry.ID
#     name: str
#     comments: str
#     students: List[Student] = strawberry.field(resolver=get_student_for_subgroup)
#
#     @classmethod
#     def from_instance(cls, instance: Subgroup) -> "Subgroup":
#         return cls(id=strawberry.ID(instance.id),
#                    name=instance.name,
#                    comments=instance.comments)
#
#
# @strawberry.type
# class SubgroupNotFound:
#     error: str = "Такой подгруппы не существует"
#
#
# SelectSubgroupResponse = strawberry.union("SelectSubgroupResponse",
#                                           (Subgroup,
#                                            SubgroupNotFound))
