from dataclass_mapper import MapperMode, create_enum_mapper, create_mapper, ignore

from todo_app.models import Tag, Todo, TodoCreate, TodoState, TodoUpdate
from todo_app.tables import Tag as TagOrm
from todo_app.tables import Todo as TodoOrm
from todo_app.tables import TodoState as TodoStateOrm

create_mapper(
    Tag,
    TagOrm,
    {
        TagOrm.tag: "root",
        TagOrm.todo_id: ignore(),
    },
)

create_mapper(
    TagOrm,
    Tag,
    {
        "root": "tag",
    },
)

create_enum_mapper(
    TodoState,
    TodoStateOrm,
)

create_enum_mapper(
    TodoStateOrm,
    TodoState,
)

create_mapper(
    TodoCreate,
    TodoOrm,
    {
        TodoOrm.id: ignore(),
        TodoOrm.state: lambda: TodoStateOrm.Ongoing,
    },
    mapper_mode=MapperMode.CREATE,
)

create_mapper(
    TodoOrm,
    Todo,
)

create_mapper(
    TodoUpdate,
    TodoOrm,
    {
        TodoOrm.id: ignore(),
        TodoOrm.tags: ignore(),
    },
    mapper_mode=MapperMode.UPDATE,
)
