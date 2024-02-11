from datetime import date
from enum import StrEnum, auto

from dataclass_mapper import MapperMode, enum_mapper, enum_mapper_from, ignore, mapper, mapper_from
from pydantic import BaseModel

from . import tables as t


@enum_mapper(t.TodoState)
@enum_mapper_from(t.TodoState)
class TodoState(StrEnum):
    Ongoing = auto()
    Finished = auto()
    Archived = auto()


@mapper(
    t.Todo,
    {t.Todo.id: ignore(), t.Todo.state: lambda: t.TodoState.Ongoing, t.Todo.tags: ignore()},
    mapper_mode=MapperMode.CREATE,
)
class TodoCreate(BaseModel):
    title: str
    description: str
    deadline: date | None = None
    tags: list[str]


@mapper_from(t.Todo, {"tags": lambda self: [tag.tag for tag in self.tags]})
class Todo(BaseModel):
    id: int
    title: str
    description: str
    deadline: date | None = None
    state: TodoState
    tags: list[str]


@mapper(t.Todo, {t.Todo.id: ignore(), t.Todo.tags: ignore()}, mapper_mode=MapperMode.UPDATE)
class TodoUpdate(BaseModel):
    title: str
    description: str
    deadline: date | None = None
    state: TodoState
    tags: list[str]
