from typing import Any, Generator

import pytest
from fastapi import Response, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config
from api import routers, schemas
from api.config import API_V1_STR, settings
from api.db import models
from api.db.database import Base, get_db
from api.main import app

from .config import (
    test_email,
    test_is_superuser,
    test_password,
    test_username,
    testpost_content,
    testpost_published,
    testpost_title,
)

preFixUser: str = routers.preFix_user

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address>:<port>/<dbname>"
# Neon database
SQLALCHEMY_DATABASE_URL: str = (
    f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASS}@{settings.DB_HOSTNAME}/{settings.DB_NAME}_test?sslmode=require"
)
# Local database
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASS}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}_test"

engine: create_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # FOLLOWING ARGUMENT IS ONLY FOR SQLITE DATABASE
    # connect_args={"check_same_thread": False},
    echo=True,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


## Alembic
# @pytest.fixture(scope="session")
# def alembic_config() -> Config:
#     # If you're using a programmatic configuration for Alembic
#     alembic_cfg = Config()
#     alembic_cfg.set_main_option("script_location", "alembic")
#     alembic_cfg.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
#     return alembic_cfg


# @pytest.fixture()
# def session(alembic_config) -> Generator[sessionmaker, Any, None]:
#     # Apply migrations at the beginning of the test session
#     command.upgrade(alembic_config, "head")

#     db: sessionmaker = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
## End Alembic


@pytest.fixture()
def session() -> Generator[sessionmaker, Any, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: sessionmaker = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session) -> Generator[sessionmaker, Any, None]:
    def override_get_db() -> Generator[sessionmaker, Any, None]:
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client) -> dict[str, str]:
    user_data: dict[str, str] = {
        "username": test_username[0],
        "email": test_email[0],
        "password": test_password[0],
        "is_superuser": test_is_superuser[0],
    }
    respoonse_fixture: Response = client.post(
        f"{API_V1_STR}{preFixUser}/create-user", json=user_data
    )
    assert respoonse_fixture.status_code == status.HTTP_201_CREATED
    new_user: Any = respoonse_fixture.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture()
def token(client, test_user) -> str:
    response: Response = client.post(
        f"{API_V1_STR}/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    access_token = schemas.Token(**response.json())
    return access_token


@pytest.fixture()
def authorized_client(client, token) -> Any:
    print(token)
    # client.headers.update({"Authorization": f"Bearer {token.access_token}"})
    client.headers = {**client.headers, "Authorization": f"Bearer {token.access_token}"}
    return client


@pytest.fixture()
def test_posts(session, test_user) -> None:
    testposts_data: list[dict[str, Any]] = [
        {
            "title": title,
            "content": content,
            "published": published,
            "owner_id": test_user["id"],
        }
        for title, content, published in zip(
            testpost_title, testpost_content, testpost_published
        )
    ]

    def create_post_model(post) -> Any:
        return models.Posts(**post)

    post_map = map(create_post_model, testposts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="title[0]", content="content[0]", published=published[0]),
    # models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])

    session.commit()

    posts: Any = session.query(models.Posts).all()
    return posts
