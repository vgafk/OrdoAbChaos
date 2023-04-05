from typing import Optional, List
import strawberry

from attendance.resolvers import get_attendace_by_student
from attendance.types import Attendance
from sql import Students

# from groups.types import Group, Subgroup
# from groups.resolvers import get_group_for_student, get_subgroup_for_student


@strawberry.input
class StudentGetInput:
    id: Optional[int] = strawberry.UNSET
    surname: Optional[str] = strawberry.UNSET
    name: Optional[str] = strawberry.UNSET
    middle_name: Optional[str] = strawberry.UNSET
    snils: Optional[str] = strawberry.UNSET

    def is_empty(self):
        return not any([self.id, self.surname, self.name, self.middle_name, self.snils])


@strawberry.type
class Student:
    id: strawberry.ID
    surname: str
    name: str
    middle_name: str
    snils: str
    attendance: List[Attendance] = strawberry.field(resolver=get_attendace_by_student)
    # group: List[Group] = strawberry.field(resolver=get_group_for_student)
    # subgroups: Optional[List[Subgroup]] = strawberry.field(resolver=get_subgroup_for_student)

    @classmethod
    def from_instance(cls, instance: Students) -> "Student":
        return cls(id=strawberry.ID(instance.id),
                   surname=instance.surname,
                   name=instance.name,
                   middle_name=instance.middle_name,
                   snils=instance.snils)