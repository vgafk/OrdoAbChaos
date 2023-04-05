from typing import List

import strawberry

from faculties.resolvers import get_faculties
from faculties.types import Faculty
from groups.types import Group, Subgroup
from schedule.types import Lesson
from students.resolvers import get_students
from groups.resolvers import get_groups, get_subgroups
from students.types import Student


@strawberry.type
class Query:
    students: List[Student] = strawberry.field(resolver=get_students)
    groups: List[Group] = strawberry.field(resolver=get_groups)
    subgroups: List[Subgroup] = strawberry.field(resolver=get_subgroups)
    faculties: List[Faculty] = strawberry.field(resolver=get_faculties)
    # week_schedule: List[Lesson] = strawberry.field(resolver=get_groups_lessons_by_week)
