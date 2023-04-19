from typing import Optional, List
import strawberry

from groups.resolvers import get_group_for_faculty
from groups.types import Group
from sql import Faculty


@strawberry.input
class FacultiesGetInput:
    id: Optional[int] = strawberry.UNSET
    name: Optional[str] = strawberry.UNSET

    def is_empty(self):
        return not any([self.id, self.name])


@strawberry.type
class Faculty:
    id: strawberry.ID
    name: str
    full_name: str
    groups: List[Group] = strawberry.field(resolver=get_group_for_faculty)

    @classmethod
    def from_instance(cls, instance: Faculty) -> "Faculty":
        return cls(id=strawberry.ID(instance.id),
                   name=instance.name,
                   full_name=instance.full_name)
