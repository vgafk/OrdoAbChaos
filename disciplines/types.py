import strawberry

from sql import Discipline


# @strawberry.input
# class FacultiesGetInput:
#     id: Optional[int] = strawberry.UNSET
#     name: Optional[str] = strawberry.UNSET
#
#     def is_empty(self):
#         return not any([self.id, self.name])


@strawberry.type
class Discipline:
    id: strawberry.ID
    name: str

    @classmethod
    def from_instance(cls, instance: Discipline) -> "Discipline":
        return cls(id=strawberry.ID(instance.id),
                   name=instance.name)


@strawberry.type
class DisciplineNotFound:
    error: str = "Дисциплина не найдена"


SelectDisciplineResponse = strawberry.union("SelectDisciplineResponse",
                                            (Discipline,
                                             DisciplineNotFound))
