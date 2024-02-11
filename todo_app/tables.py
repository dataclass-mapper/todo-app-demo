from datetime import date
from enum import Enum, unique

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todo_app.database import Base


@unique
class TodoState(Enum):
    Ongoing = 1
    Finished = 2
    Archived = 3


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(length=88))
    description: Mapped[str] = mapped_column()
    deadline: Mapped[date | None] = mapped_column()
    state: Mapped[TodoState] = mapped_column()

    tags: Mapped[list["Tag"]] = relationship(order_by="Tag.tag", cascade="save-update, merge, delete, delete-orphan")


class Tag(Base):
    __tablename__ = "tags"

    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id"), primary_key=True)
    tag: Mapped[str] = mapped_column(String(64), primary_key=True)
