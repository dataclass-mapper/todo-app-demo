from asyncio import get_event_loop
from datetime import date

from todo_app.database import AsyncSessionLocal
from todo_app.tables import Tag as TagOrm
from todo_app.tables import Todo as TodoOrm
from todo_app.tables import TodoState as TodoStateOrm


async def seed():
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

    db = AsyncSessionLocal()
    db.add_all([grocery_todo, release_todo, optimize_todo])
    await db.commit()


def main():
    loop = get_event_loop()
    loop.run_until_complete(seed())


if __name__ == "__main__":
    main()
