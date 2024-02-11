from datetime import date

from dataclass_mapper import MapperMode, create_mapper, ignore, mapper, mapper_from
from pydantic import BaseModel, RootModel

from . import tables as t

Tag = RootModel[str]


create_mapper(t.Tag, Tag, {"root": "tag"})
create_mapper(Tag, t.Tag, {t.Tag.tag: "root", t.Tag.todo_id: ignore()})


@mapper(
    t.Todo,
    {t.Todo.id: ignore(), t.Todo.state: lambda: t.TodoState.Ongoing},
    mapper_mode=MapperMode.CREATE,
)
class TodoCreate(BaseModel):
    title: str
    description: str
    deadline: date | None = None
    tags: list[Tag]


@mapper_from(t.Todo)
class Todo(BaseModel):
    id: int
    title: str
    description: str
    deadline: date | None = None
    state: t.TodoState
    tags: list[Tag]


@mapper(t.Todo, {t.Todo.id: ignore(), t.Todo.tags: ignore()}, mapper_mode=MapperMode.UPDATE)
class TodoUpdate(BaseModel):
    title: str
    description: str
    deadline: date | None = None
    state: t.TodoState
    tags: list[Tag]
