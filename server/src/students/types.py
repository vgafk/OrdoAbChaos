from typing import Optional, List, TYPE_CHECKING
import strawberry

from attendance.resolvers import get_attendace_by_student
from attendance.types import Attendance
from sql import Students


@strawberry.input
class StudentGetInput:
    id: Optional[int] = strawberry.UNSET
    surname: Optional[str] = strawberry.UNSET
    name: Optional[str] = strawberry.UNSET
    middle_name: Optional[str] = strawberry.UNSET
    snils: Optional[str] = strawberry.UNSET
    email: Optional[str] = strawberry.UNSET
    finance_form: Optional[int] = strawberry.UNSET
    group_id: Optional[str] = strawberry.UNSET


@strawberry.type
class NewStudentInput:
    id: Optional[int] = strawberry.UNSET
    surname: str
    name: str
    middle_name: Optional[str] = strawberry.UNSET
    snils: Optional[str] = strawberry.UNSET
    email: Optional[str] = strawberry.UNSET
    finance_form: Optional[int] = strawberry.UNSET
    group_id: Optional[str] = strawberry.UNSET

    @classmethod
    def from_instance(cls, instance: Students, group_id: int = None) -> "NewStudentInput":
        return cls(id=strawberry.ID(instance.id),
                   surname=instance.surname,
                   name=instance.name,
                   middle_name=instance.middle_name,
                   snils=instance.snils,
                   email=instance.email,
                   finance_form=instance.finance_form_id,
                   group_id=group_id)


@strawberry.type
class Student:
    id: strawberry.ID
    surname: str
    name: str
    middle_name: str
    snils: str
    attendance: List[Attendance] = strawberry.field(resolver=get_attendace_by_student)

    @classmethod
    def from_instance(cls, instance: Students) -> "Student":
        return cls(id=strawberry.ID(instance.id),
                   surname=instance.surname,
                   name=instance.name,
                   middle_name=instance.middle_name,
                   snils=instance.snils)