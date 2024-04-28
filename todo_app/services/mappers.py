from dataclass_mapper import MapperMode, create_enum_mapper, create_mapper, ignore

from todo_app.models import Tag, Todo, TodoCreate, TodoState, TodoUpdate
from todo_app.tables import TagOrm, TodoOrm, TodoStateOrm

###################
# Mapper for tags #
###################

create_mapper(
    Tag,
    TagOrm,
    {
        TagOrm.tag: "",
        TagOrm.todo_id: ignore(),
    },
)

create_mapper(
    TagOrm,
    Tag,
    {
        "": "tag",
    },
)

#########################
# Mapper for state enum #
#########################

create_enum_mapper(
    TodoState,
    TodoStateOrm,
)

create_enum_mapper(
    TodoStateOrm,
    TodoState,
)

####################
# Mapper for Todos #
####################

# fetch Todo from database
create_mapper(
    TodoOrm,
    Todo,
)

# create new Todo in Ongoing state
create_mapper(
    TodoCreate,
    TodoOrm,
    {
        TodoOrm.id: ignore(),
        TodoOrm.state: lambda: TodoStateOrm.Ongoing,
    },
    mapper_mode=MapperMode.CREATE,
)

# update an existing todo
create_mapper(
    TodoUpdate,
    TodoOrm,
    {
        TodoOrm.id: ignore(),
        # map tags later in order to update existing tags instead of recreating them
        TodoOrm.tags: ignore(),
    },
    mapper_mode=MapperMode.UPDATE,
)
