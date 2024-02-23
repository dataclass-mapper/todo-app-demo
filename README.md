# Todo-App

A small example application for demonstrating and testing the dataclass-mapper library.

```bash
# install depencies
poetry install --sync --with=dev

# create database
poetry run alembic upgrade head

# seed database with some example data
poetry run seed

# run the backend application
poetry run app
```
