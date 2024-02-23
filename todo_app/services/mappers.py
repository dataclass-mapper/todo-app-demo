from dataclass_mapper import MapperMode, create_enum_mapper, create_mapper, ignore

from todo_app import models as m
from todo_app import tables as t

create_mapper(
    m.Tag,
    t.Tag,
    {
        t.Tag.tag: "root",
        t.Tag.todo_id: ignore(),
    },
)

create_mapper(
    t.Tag,
    m.Tag,
    {
        "root": "tag",
    },
)

create_enum_mapper(
    m.TodoState,
    t.TodoState,
)

create_enum_mapper(
    t.TodoState,
    m.TodoState,
)

create_mapper(
    m.TodoCreate,
    t.Todo,
    {
        t.Todo.id: ignore(),
        t.Todo.state: lambda: t.TodoState.Ongoing,
    },
    mapper_mode=MapperMode.CREATE,
)

create_mapper(
    t.Todo,
    m.Todo,
)

create_mapper(
    m.TodoUpdate,
    t.Todo,
    {
        t.Todo.id: ignore(),
        t.Todo.tags: ignore(),
    },
    mapper_mode=MapperMode.UPDATE,
)
