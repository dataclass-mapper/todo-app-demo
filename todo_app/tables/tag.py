from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from todo_app.database import Base


class TagOrm(Base):
    __tablename__ = "tags"

    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id"), primary_key=True)
    tag: Mapped[str] = mapped_column(String(64), primary_key=True)


Index("idx_tags_todo_id", TagOrm.todo_id)
