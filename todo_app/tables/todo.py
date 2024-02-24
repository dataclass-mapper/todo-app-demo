from datetime import date
from enum import StrEnum, auto, unique
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todo_app.database import Base

if TYPE_CHECKING:
    from .tag import TagOrm


@unique
class TodoStateOrm(StrEnum):
    Ongoing = auto()
    Finished = auto()
    Archived = auto()


class TodoOrm(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(length=88))
    description: Mapped[str] = mapped_column()
    deadline: Mapped[date | None] = mapped_column()
    state: Mapped[TodoStateOrm] = mapped_column()

    tags: Mapped[list["TagOrm"]] = relationship(
        order_by="TagOrm.tag", cascade="save-update, merge, delete, delete-orphan", lazy="immediate"
    )
