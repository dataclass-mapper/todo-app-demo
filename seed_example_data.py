from datetime import date

from todo_app import tables as t
from todo_app.database import Base, SessionLocal, engine


def main():
    Base.metadata.create_all(bind=engine)

    grocery_todo = t.Todo(
        title="Go grocery shopping",
        description="Bread, Butter, Cheese, Milk",
        deadline=date(2024, 2, 12),
        state=t.TodoState.Ongoing,
        tags=[t.Tag(tag="home")],
    )
    release_todo = t.Todo(
        title="Release v2 library",
        description="Release v2 of the dataclass_mapper library",
        deadline=date(2024, 2, 28),
        state=t.TodoState.Ongoing,
        tags=[t.Tag(tag="development"), t.Tag(tag="opensource")],
    )
    optimize_todo = t.Todo(
        title="Optimize generated code",
        description="The generated mapper code can be a bit inefficient, optimize it.",
        deadline=date(2024, 4, 30),
        state=t.TodoState.Ongoing,
        tags=[t.Tag(tag="development"), t.Tag(tag="opensource")],
    )

    db = SessionLocal()
    db.add_all([grocery_todo, release_todo, optimize_todo])
    db.commit()
