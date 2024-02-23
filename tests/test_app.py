import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from todo_app.main import app, get_db
from todo_app.tables import Base


@pytest.fixture
def client():
    SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite://"

    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        # poolclass=StaticPool,
        echo=True,
    )
    TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

    async def override_get_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        db = TestingSessionLocal()
        try:
            yield db
        finally:
            await db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


def test_create_todo(client: TestClient):
    response = client.post(
        "/todos",
        json={
            "title": "Todo1",
            "description": "Some description",
            "deadline": "2024-02-11",
            "tags": ["tag1", "tag2"],
        },
    )

    expected = {
        "id": 1,
        "title": "Todo1",
        "description": "Some description",
        "deadline": "2024-02-11",
        "tags": ["tag1", "tag2"],
        "state": "ongoing",
    }
    assert response.status_code == 200, response.text
    assert response.json() == expected

    response = client.get("/todos/1")
    assert response.status_code == 200, response.text
    assert response.json() == expected


def test_list_todos(client: TestClient):
    for i in range(1, 3):
        response = client.post(
            "/todos",
            json={
                "title": f"Todo{i}",
                "description": "Some description",
                "deadline": "2024-02-11",
                "tags": ["common_tag", f"tag{i}"],
            },
        )
        assert response.status_code == 200, response.text

    response = client.get("/todos")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "id": 1,
            "title": "Todo1",
            "description": "Some description",
            "deadline": "2024-02-11",
            "tags": ["common_tag", "tag1"],
            "state": "ongoing",
        },
        {
            "id": 2,
            "title": "Todo2",
            "description": "Some description",
            "deadline": "2024-02-11",
            "tags": ["common_tag", "tag2"],
            "state": "ongoing",
        },
    ]

    response = client.get("/todos", params={"tag": "common_tag"})
    assert response.status_code == 200, response.text
    assert [todo["id"] for todo in response.json()] == [1, 2]

    response = client.get("/todos", params={"tag": "tag2"})
    assert response.status_code == 200, response.text
    assert [todo["id"] for todo in response.json()] == [2]

    response = client.get("/todos", params={"state": "ongoing"})
    assert response.status_code == 200, response.text
    assert [todo["id"] for todo in response.json()] == [1, 2]

    response = client.get("/todos", params={"state": "finished"})
    assert response.status_code == 200, response.text
    assert [todo["id"] for todo in response.json()] == []


def test_update_todo(client: TestClient):
    response = client.post(
        "/todos",
        json={
            "title": "Todo1",
            "description": "Some description",
            "deadline": "2024-02-11",
            "tags": ["tag1", "tag2"],
        },
    )
    assert response.status_code == 200, response.text

    response = client.patch(
        "/todos/1",
        json={
            "title": "Todo1",
            "description": "Some description",
            "deadline": "2024-02-28",
            "tags": ["tag1", "default"],
            "state": "finished",
        },
    )

    expected = {
        "id": 1,
        "title": "Todo1",
        "description": "Some description",
        "deadline": "2024-02-28",
        "tags": ["default", "tag1"],
        "state": "finished",
    }
    assert response.status_code == 200, response.text
    assert response.json() == expected

    response = client.get("/todos/1")
    assert response.status_code == 200, response.text
    assert response.json() == expected


def test_list_tags(client: TestClient):
    for i in range(1, 3):
        response = client.post(
            "/todos",
            json={
                "title": f"Todo{1}",
                "description": "Some description",
                "deadline": "2024-02-11",
                "tags": ["common_tag", f"tag{i}"],
            },
        )
        assert response.status_code == 200, response.text

    response = client.get("/tags")
    assert response.status_code == 200, response.text
    assert response.json() == ["common_tag", "tag1", "tag2"] or ["common_tag", "tag1", "tag2"]
