from typing import Optional
import strawberry

from sql import Teacher

@strawberry.type
class Teacher:
    id: strawberry.ID
    surname: str
    name: Optional[str]
    middle_name: Optional[str]

    @classmethod
    def from_instance(cls, instance: Teacher) -> "Teacher":
        return cls(id=strawberry.ID(instance.id),
                   surname=instance.surname,
                   name=instance.name,
                   middle_name=instance.middle_name)


@strawberry.type
class TeacherNotFound:
    error: str = "Преподаватель не найден"
    not_set_error: str = "Преподаватель не назначен"


SelectTeacherResponse = strawberry.union("SelectTeacherResponse",
                                         (Teacher,
                                          TeacherNotFound))
