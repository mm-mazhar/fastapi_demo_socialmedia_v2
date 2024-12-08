from typing import Any

import pytest
from dateutil import parser
from fastapi import Response, status

from api import routers, schemas
from api.config import API_V1_STR

# Assuming .config and .conftest are correctly set up and imported
from .config import testpost_content, testpost_published, testpost_title, username

# don't need to import since every test looks for conftest.py file and it's components
# from .conftest import client, session

preFixPost: str = routers.preFix_post


# Test Get Posts
def test_get_posts(authorized_client, test_posts) -> None:
    response: Response = authorized_client.get(f"{API_V1_STR}{preFixPost}/get")
    response_data: Any = response.json()

    def validate(post) -> Any:
        return schemas.ResponseBase(**post)

    posts_map = map(validate, response_data)
    response_validated = list(posts_map)
    print(f"Validated Response: {response_validated}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) > 0
    # print(response_data)
    for i in range(len(response_data)):
        assert response_data[i].get("title") == test_posts[i].title
        assert response_data[i].get("content") == test_posts[i].content
        assert response_data[i].get("published") == test_posts[i].published


# Test Create Post
@pytest.mark.parametrize(
    "test_post_title, test_post_content, test_post_published",
    [
        (testpost_title, testpost_content, testpost_published)
        for testpost_title, testpost_content, testpost_published in zip(
            testpost_title, testpost_content, testpost_published
        )
    ],
)
def test_create_post(
    authorized_client,
    # test_user,
    test_post_title,
    test_post_content,
    test_post_published,
) -> None:
    data: dict[str, Any] = {
        "title": test_post_title,
        "content": test_post_content,
        "published": test_post_published,
        # "owner_id": test_user["id"],
    }
    response: Response = authorized_client.post(
        f"{API_V1_STR}{preFixPost}/create",
        json=data,
    )
    response_data: Any = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    print(f"Response Data: {response_data}")
    assert response_data.get("title") == test_post_title
    assert response_data.get("content") == test_post_content
    assert response_data.get("published") == test_post_published


# Test Get Post By ID
def test_get_post_by_id(authorized_client, test_posts) -> None:
    # print(f"Test Posts: {test_posts}")
    id = 1
    response: Response = authorized_client.get(f"{API_V1_STR}{preFixPost}/id/1")
    response_data: Any = response.json()
    assert response.status_code == status.HTTP_200_OK


# Test Last Post
def test_get_post_latest(authorized_client, test_posts) -> None:
    response: Response = authorized_client.get(f"{API_V1_STR}{preFixPost}/latest")
    response_data: Any = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_data.get("title") == test_posts[-1].title
    assert response_data.get("content") == test_posts[-1].content
    assert response_data.get("published") == test_posts[-1].published


# Test Delete Post by Id
def test_delete_post_by_id(authorized_client, test_posts) -> None:
    # print(f"Test Posts: {test_posts}")
    # print(f"Test Posts 0 title: {test_posts[-1].title}")
    response: Response = authorized_client.delete(f"{API_V1_STR}{preFixPost}/delete/2")
    assert response.status_code == status.HTTP_204_NO_CONTENT


# Test Update Post by Id
def test_update_post_by_id(
    authorized_client,
    test_posts,
) -> None:
    data: dict[str, Any] = {
        "title": test_posts[0].title + " updated",
        "content": test_posts[0].content + " updated",
        "published": not test_posts[0].published,
    }
    response: Response = authorized_client.put(
        f"{API_V1_STR}{preFixPost}/update/1",
        json=data,
    )
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["title"] == data.get("title")
    assert response.json()["content"] == data.get("content")
    assert response.json()["published"] == data.get("published")


# Test Unauthorized Access
def test_unauthorized_access(client, test_user, test_posts) -> None:
    response: Response = client.get(f"{API_V1_STR}{preFixPost}/get")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response: Response = client.post(f"{API_V1_STR}{preFixPost}/create")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response: Response = client.get(f"{API_V1_STR}{preFixPost}/id/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response: Response = client.get(f"{API_V1_STR}{preFixPost}/latest")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response: Response = client.delete(f"{API_V1_STR}{preFixPost}/delete/2")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response: Response = client.put(f"{API_V1_STR}{preFixPost}/update/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
