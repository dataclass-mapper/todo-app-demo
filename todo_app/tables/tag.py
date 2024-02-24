from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from todo_app.database import Base


class TagOrm(Base):
    __tablename__ = "tags"

    todo_id: Mapped[int] = mapped_column(ForeignKey("todos.id"), primary_key=True, index=True)
    tag: Mapped[str] = mapped_column(String(64), primary_key=True)
