from typing import Any, Optional

import pytest
from fastapi import Response, status
from jose import jwt

from api import schemas
from api.config import API_V1_STR, settings

# don't need to import since every test looks for conftest.py file and it's components
# from .conftest import client, session, test_user


def test_login_user(client, test_user) -> None:
    response: Response = client.post(
        f"{API_V1_STR}/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    login_response = schemas.Token(**response.json())
    payload: dict[str, Any] = jwt.decode(
        login_response.access_token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    id: Optional[int] = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == status.HTTP_200_OK


# Test Data Validation
@pytest.mark.parametrize(
    "email, password",
    [
        ("testmail@gmail.com", "wrongpassword"),
        (None, "password123"),
        ("testmail@gmail.com", None),
    ],
)
def test_incorrect_login(test_user, client, email, password) -> None:
    response: Response = client.post(
        f"{API_V1_STR}/login", data={"username": email, "password": password}
    )
    try:
        if response.status_code == status.HTTP_403_FORBIDDEN:
            assert response.json().get("detail") == "Invalid Credentials"
    except Exception as e:
        print("\n")
        print("*" * 120)
        print("Validation Error: ", e)
        # assert some pydantic validation errors

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        print("*" * 120)
