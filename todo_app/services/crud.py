from dataclass_mapper import map_to
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from todo_app.exceptions import NotFoundException
from todo_app.models import Tag, Todo, TodoCreate, TodoState, TodoUpdate
from todo_app.tables import TagOrm, TodoOrm, TodoStateOrm


async def get_todo(db: AsyncSession, todo_id: int) -> Todo:
    """Fetch a single todo by id"""
    query = select(TodoOrm).options(selectinload(TodoOrm.tags)).filter(TodoOrm.id == todo_id)
    todo = await db.scalar(query)
    if not todo:
        raise NotFoundException("Todo", todo_id)
    return map_to(todo, Todo)


async def get_todos(db: AsyncSession, state: TodoState | None, tag: str | None) -> list[Todo]:
    """Fetch a list of all todos"""
    query = select(TodoOrm).options(selectinload(TodoOrm.tags))
    if state:
        db_state = map_to(state, TodoStateOrm)
        query = query.filter(TodoOrm.state == db_state)
    if tag:
        query = query.filter(TodoOrm.tags.any(TagOrm.tag == tag))

    todos = await db.stream_scalars(query)
    return [map_to(todo, Todo) async for todo in todos]


async def create_todo(db: AsyncSession, todo_create: TodoCreate) -> Todo:
    """Create a new todo and insert it into the database"""
    # async with db.begin():
    todo = map_to(todo_create, TodoOrm)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return map_to(todo, Todo)


async def update_todo(db: AsyncSession, todo_id: int, todo_update: TodoUpdate) -> Todo:
    """Update a todo"""
    query = select(TodoOrm).options(selectinload(TodoOrm.tags)).filter(TodoOrm.id == todo_id)
    todo = await db.scalar(query)
    if not todo:
        raise NotFoundException("Todo", todo_id)

    map_to(todo_update, todo)

    db_tags: list[TagOrm] = []
    existing_tags = {tag.tag: tag for tag in todo.tags}
    for tag in todo_update.tags:
        db_tags.append(existing_tags.get(tag.root) or map_to(tag, TagOrm))
    todo.tags = db_tags

    await db.commit()
    await db.refresh(todo)

    return map_to(todo, Todo)


async def get_tags(db: AsyncSession) -> list[Tag]:
    """Get list of all tags"""
    query = select(TagOrm.tag).group_by(TagOrm.tag).order_by(func.count(TagOrm.tag).desc())
    tags = await db.stream_scalars(query)
    return [Tag(tag) async for tag in tags]
