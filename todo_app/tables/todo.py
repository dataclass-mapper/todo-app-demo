from datetime import date
from enum import StrEnum, auto, unique
from typing import TYPE_CHECKING

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todo_app.database import Base

if TYPE_CHECKING:
    from .tag import Tag


@unique
class TodoState(StrEnum):
    Ongoing = auto()
    Finished = auto()
    Archived = auto()


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=88))
    description: Mapped[str] = mapped_column()
    deadline: Mapped[date | None] = mapped_column()
    state: Mapped[TodoState] = mapped_column()

    tags: Mapped[list["Tag"]] = relationship(
        order_by="Tag.tag", cascade="save-update, merge, delete, delete-orphan", lazy="immediate"
    )


Index("idx_todos_id", Todo.id)
