from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from sqlalchemy.orm import Session

from todo_app.exceptions import NotFoundException

from . import database, models
from .services import crud

app = FastAPI(title="Todo App", docs_url="/")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos", tags=["todo"])
def get_list_of_todos(
    state: Annotated[models.TodoState | None, Query()] = None,
    tag: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db),
) -> list[models.Todo]:
    return crud.get_todos(db, state=state, tag=tag)


@app.get("/todos/{todo_id}", tags=["todo"])
def get_todo_by_id(todo_id: int, db: Session = Depends(get_db)) -> models.Todo:
    return crud.get_todo(db, todo_id)


@app.post("/todos", tags=["todo"])
def create_new_todo(todo_create: models.TodoCreate, db: Session = Depends(get_db)) -> models.Todo:
    return crud.create_todo(db, todo_create)


@app.patch("/todos/{todo_id}", tags=["todo"])
def update_todo(todo_id: int, todo_update: models.TodoUpdate, db: Session = Depends(get_db)) -> models.Todo:
    return crud.update_todo(db, todo_id, todo_update)


@app.get("/tags", tags=["tag"])
def get_list_of_tags(db: Session = Depends(get_db)) -> list[models.Tag]:
    return crud.get_tags(db)


@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    raise HTTPException(status_code=404, detail=f"{exc.entity} with id {exc.id} was not found.")


def start():
    """Launched with `poetry run app` at root level"""
    uvicorn.run("todo_app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    start()
