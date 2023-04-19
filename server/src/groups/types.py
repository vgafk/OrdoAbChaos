from typing import Optional, List, TYPE_CHECKING
import strawberry

from schedule.resolvers import get_groups_lessons_by_group
from schedule.types import Lesson
from sql import Group, Subgroup
from students.resolvers import get_student_for_group, get_student_for_subgroup
from students.types import Student


@strawberry.input
class GroupGetInput:
    id: Optional[int] = strawberry.UNSET
    name: Optional[str] = strawberry.UNSET
    schedule_week: Optional[int] = strawberry.UNSET


@strawberry.type
class Group:
    id: strawberry.ID
    name: str
    full_name: str
    students: List["Student"] = strawberry.field(resolver=get_student_for_group)
    week_schedule: List[Lesson] = strawberry.field(resolver=get_groups_lessons_by_group)

    @classmethod
    def from_instance(cls, instance: Group) -> "Group":
        return cls(id=strawberry.ID(instance.id),
                   name=instance.name,
                   full_name=instance.full_name)


@strawberry.input
class SubgroupGetInput:
    id: Optional[int] = strawberry.UNSET
    name: Optional[str] = strawberry.UNSET

    def is_empty(self):
        return not any([self.id, self.name])


@strawberry.type
class Subgroup:
    id: strawberry.ID
    name: str
    comments: str
    students: List["Student"] = strawberry.field(resolver=get_student_for_subgroup)

    @classmethod
    def from_instance(cls, instance: Subgroup) -> "Subgroup":
        return cls(id=strawberry.ID(instance.id),
                   name=instance.name,
                   comments=instance.comments)