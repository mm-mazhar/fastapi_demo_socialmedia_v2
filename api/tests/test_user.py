import datetime
from typing import Any

import pytest
from dateutil import parser
from fastapi import Response, status

# from api.routers.user import preFix_user
from api import routers
from api.config import API_V1_STR

# Assuming .config and .conftest are correctly set up and imported
from .config import (
    email,
    is_active,
    is_superuser,
    password,
    test_email,
    test_is_active,
    test_is_superuser,
    test_password,
    test_username,
    username,
)

preFixUser: str = routers.preFix_user

# don't need to import since every test looks for conftest.py file and it's components
# from .conftest import client, session


# Test Create User
@pytest.mark.parametrize(
    "test_username, test_email, test_password, test_is_active, test_is_superuser",
    [
        (username, email, password, is_active, is_superuser)
        for username, email, password, is_active, is_superuser in zip(
            username, email, password, is_active, is_superuser
        )
    ],
)
def test_create_user(
    client, test_username, test_email, test_password, test_is_active, test_is_superuser
) -> None:
    data: dict[str, str] = {
        "username": test_username,
        "email": test_email,
        "password": test_password,
        "is_active": test_is_active,
        "is_superuser": test_is_superuser,
    }
    response: Response = client.post(
        f"{API_V1_STR}{preFixUser}/create-user",
        json=data,
    )
    response_data: Any = response.json()
    # print("*" * 120)
    # print("Response Data: ", response_data)
    # print("*" * 120)
    assert response.status_code == status.HTTP_201_CREATED
    user_created_at_datetime: datetime = parser.parse(
        str(response_data.get("user_created_at"))
    )
    assert isinstance(user_created_at_datetime, datetime.datetime)
    assert response_data["username"] == test_username
    assert response_data["email"] == test_email
    assert response_data["is_active"] == test_is_active
    assert response_data["is_superuser"] == test_is_superuser


# Test Data Validation
@pytest.mark.parametrize(
    "test_username, test_email, test_password, test_is_active, test_is_superuser",
    [
        ("ad", "testemail@gmail.com", "Password123!", True, False),
        ("testusername", "testemailgmail.com", "Password@123!", True, True),
        ("testusername", "testemail@gmail.com", "password123", False, False),
        ("testusername", "testemail@hotmail.com", "Password123!", None, True),
        ("testusername", "testemail@gmail.com", "Password123!", True, None),
        # ("testusername", "testemail@gmail.com", "Password123@", True, True), # This should fail
    ],
)
def test_create_user_invalid_data(
    client, test_username, test_email, test_password, test_is_active, test_is_superuser
) -> None:
    data: dict[str, str] = {
        "username": test_username,
        "email": test_email,
        "password": test_password,
        "is_active": test_is_active,
        "is_superuser": test_is_superuser,
    }
    response: Response = client.post(
        f"{API_V1_STR}{preFixUser}/create-user",
        json=data,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# Test Get User by Username
def test_get_user_by_username(
    authorized_client,
) -> None:
    response: Response = authorized_client.get(
        # f"{API_V1_STR}{preFixUser}/get?limit=100&skip=0&search=abc"
        f"{API_V1_STR}{preFixUser}/get?limit=100&skip=0&search={test_username[0]}"
    )  # Comming from excel file from .config import import test_username
    assert response.status_code == status.HTTP_200_OK
    # assert response.json()[0]["username"] == "abc"
    assert response.json()[0]["username"] == test_username[0]


# Test Update User by Username
def test_update_user_by_username(
    authorized_client,
) -> None:
    response: Response = authorized_client.put(
        f"{API_V1_STR}{preFixUser}/update/{test_username[0]}",
        json={
            "username": test_username[0] + "updated",
            "email": test_email[0],
            "password": test_password[0],
            "is_active": test_is_active[0],
            "is_superuser": test_is_superuser[0],
        },
    )
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["username"] == test_username[0] + "updated"
    assert response.json()["email"] == test_email[0]


# Test Delete User by ID
def test_delete_user_by_id(
    authorized_client,
) -> None:
    response: Response = authorized_client.delete(
        f"{API_V1_STR}{preFixUser}/delete/id/{1}",  # ID of the user to delete is hardcoded for now
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


# Test Delete User by Username
def test_delete_user_by_username(
    authorized_client,
) -> None:
    response: Response = authorized_client.delete(
        f"{API_V1_STR}{preFixUser}/delete/{test_username[0]}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
