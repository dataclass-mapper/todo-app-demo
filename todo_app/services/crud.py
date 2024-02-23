from dataclass_mapper import map_to
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from todo_app.exceptions import NotFoundException
from todo_app.models import Tag, Todo, TodoCreate, TodoState, TodoUpdate
from todo_app.tables import Tag as TagOrm
from todo_app.tables import Todo as TodoOrm
from todo_app.tables import TodoState as TodoStateOrm


def get_todo(db: Session, todo_id: int) -> Todo:
    """Fetch a single todo by id"""
    todo = db.query(TodoOrm).options(selectinload(TodoOrm.tags)).filter(TodoOrm.id == todo_id).first()
    if not todo:
        raise NotFoundException("Todo", todo_id)
    return map_to(todo, Todo)


def get_todos(db: Session, state: TodoState | None, tag: str | None) -> list[Todo]:
    """Fetch a list of all todos"""
    query = db.query(TodoOrm).options(selectinload(TodoOrm.tags))
    if state:
        db_state = map_to(state, TodoStateOrm)
        query = query.filter(TodoOrm.state == db_state)
    if tag:
        query = query.filter(TodoOrm.tags.any(TagOrm.tag == tag))
    todos = query.all()
    return [map_to(todo, Todo) for todo in todos]


def create_todo(db: Session, todo_create: TodoCreate) -> Todo:
    """Create a new todo and insert it into the database"""
    todo = map_to(todo_create, TodoOrm)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return map_to(todo, Todo)


def update_todo(db: Session, todo_id: int, todo_update: TodoUpdate) -> Todo:
    """Update a todo"""
    todo = db.query(TodoOrm).options(selectinload(TodoOrm.tags)).filter(TodoOrm.id == todo_id).first()
    if not todo:
        raise NotFoundException("Todo", todo_id)

    map_to(todo_update, todo)

    db_tags: list[TagOrm] = []
    existing_tags = {tag.tag: tag for tag in todo.tags}
    for tag in todo_update.tags:
        db_tags.append(existing_tags.get(tag.root) or map_to(tag, TagOrm))
    todo.tags = db_tags

    db.commit()
    db.refresh(todo)
    return map_to(todo, Todo)


def find_tag(tag_orms: list[TagOrm], tag: str) -> TagOrm | None:
    for tag_orm in tag_orms:
        if tag_orm.tag == tag:
            return tag_orm
    return None


def get_tags(db: Session) -> list[Tag]:
    """Get list of all tags"""
    tag_rows = db.query(TagOrm.tag).group_by(TagOrm.tag).order_by(func.count(TagOrm.tag).desc()).all()
    return [Tag(tag[0]) for tag in tag_rows]
