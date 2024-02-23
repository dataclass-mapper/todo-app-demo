from datetime import date

from todo_app.database import SessionLocal
from todo_app.tables import Tag as TagOrm
from todo_app.tables import Todo as TodoOrm
from todo_app.tables import TodoState as TodoStateOrm


def main():
    grocery_todo = TodoOrm(
        title="Go grocery shopping",
        description="Bread, Butter, Cheese, Milk",
        deadline=date(2024, 2, 12),
        state=TodoStateOrm.Ongoing,
        tags=[TagOrm(tag="home")],
    )
    release_todo = TodoOrm(
        title="Release v2 library",
        description="Release v2 of the dataclass_mapper library",
        deadline=date(2024, 2, 28),
        state=TodoStateOrm.Ongoing,
        tags=[TagOrm(tag="development"), TagOrm(tag="opensource")],
    )
    optimize_todo = TodoOrm(
        title="Optimize generated code",
        description="The generated mapper code can be a bit inefficient, optimize it.",
        deadline=date(2024, 4, 30),
        state=TodoStateOrm.Ongoing,
        tags=[TagOrm(tag="development"), TagOrm(tag="opensource")],
    )

    db = SessionLocal()
    db.add_all([grocery_todo, release_todo, optimize_todo])
    db.commit()
