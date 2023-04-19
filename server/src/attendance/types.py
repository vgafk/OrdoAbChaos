from typing import List, Dict, Optional

import strawberry

from schedule.resolvers import get_lessons_by_id
from schedule.types import Lesson
from sql import Discipline


# @strawberry.type
# class AttendanceType:
#     id: strawberry.ID
#     name: str
#
#     @classmethod
#     def from_instance(cls, instance: AttendanceType) -> "AttendanceType":
#         return cls(id=strawberry.ID(instance.id),
#                    name=instance.name)


@strawberry.type
class Attendance:
    id: strawberry.ID
    lesson_id: int
    lesson: Lesson = strawberry.field(resolver=get_lessons_by_id)
    attendance_type_id: int
    # attendance_type = strawberry.field(resolver=get_attendace_type)

    @classmethod
    def from_instance(cls, instance: Discipline) -> "Discipline":
        return cls(id=strawberry.ID(instance.id),
                   lesson_id=instance.schedule_id,
                   attendance_type_id=instance.attendance_type_id)

@strawberry.input
class AttendanceListInput:
    reason: int
    ids: Optional[List[int]] = strawberry.UNSET
    lesson_id: Optional[int] = strawberry.UNSET
    student_id: Optional[int] = strawberry.UNSET


@strawberry.input
class SaveDataInput:
    deleted: List[int]
    updated: List[AttendanceListInput]
    added: List[AttendanceListInput]

# @strawberry.type
# class DisciplineNotFound:
#     error: str = "Дисциплина не найдена"
#
#
# SelectDisciplineResponse = strawberry.union("SelectDisciplineResponse",
#                                             (Discipline,
#                                              DisciplineNotFound))
