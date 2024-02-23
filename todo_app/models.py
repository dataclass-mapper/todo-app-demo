from datetime import date
from enum import StrEnum, auto

from pydantic import BaseModel, RootModel

Tag = RootModel[str]


class TodoState(StrEnum):
    Ongoing = auto()
    Finished = auto()
    Archived = auto()


class TodoCreate(BaseModel):
    title: str
    description: str
    deadline: date | None = None
    tags: list[Tag]


class Todo(BaseModel):
    id: int
    title: str
    description: str
    deadline: date | None = None
    state: TodoState
    tags: list[Tag]


class TodoUpdate(BaseModel):
    title: str
    description: str
    deadline: date | None = None
    state: TodoState
    tags: list[Tag]
