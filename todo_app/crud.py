from dataclass_mapper import map_to
from sqlalchemy import func
from sqlalchemy.orm import Session

from todo_app.exceptions import NotFoundException

from . import models as m
from . import tables as t


def get_todo(db: Session, todo_id: int) -> m.Todo:
    """Fetch a single todo by id"""
    todo = db.query(t.Todo).filter(t.Todo.id == todo_id).first()
    if not todo:
        raise NotFoundException("Todo", todo_id)
    return map_to(todo, m.Todo)


def get_todos(db: Session, state: t.TodoState | None, tag: str | None) -> list[m.Todo]:
    """Fetch a list of all todos"""
    query = db.query(t.Todo)
    if state:
        query = query.filter(t.Todo.state == state)
    if tag:
        query = query.filter(t.Todo.tags.any(t.Tag.tag == tag))
    todos = query.all()
    return [map_to(todo, m.Todo) for todo in todos]


def create_todo(db: Session, todo_create: m.TodoCreate) -> m.Todo:
    """Create a new todo and insert it into the database"""
    todo = map_to(todo_create, t.Todo)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return map_to(todo, m.Todo)


def update_todo(db: Session, todo_id: int, todo_update: m.TodoUpdate) -> m.Todo:
    """Update a todo"""
    todo = db.query(t.Todo).filter(t.Todo.id == todo_id).first()
    if not todo:
        raise NotFoundException("Todo", todo_id)

    map_to(todo_update, todo)

    db_tags: list[t.Tag] = []
    existing_tags = {tag.tag: tag for tag in todo.tags}
    for tag in todo_update.tags:
        db_tags.append(existing_tags.get(tag.root) or map_to(tag, t.Tag))
    todo.tags = db_tags

    db.commit()
    db.refresh(todo)
    return map_to(todo, m.Todo)


def find_tag(tag_orms: list[t.Tag], tag: str) -> t.Tag | None:
    for tag_orm in tag_orms:
        if tag_orm.tag == tag:
            return tag_orm
    return None


def get_tags(db: Session) -> list[m.Tag]:
    """Get list of all tags"""
    tag_rows = db.query(t.Tag.tag).group_by(t.Tag.tag).order_by(func.count(t.Tag.tag).desc()).all()
    return [m.Tag(tag[0]) for tag in tag_rows]
