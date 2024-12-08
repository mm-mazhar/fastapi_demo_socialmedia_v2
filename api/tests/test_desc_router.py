import pytest
from fastapi import Response, status
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api import schemas
from api.config import API_PROJECT_NAME, API_V1_STR, __version__, package_version
from api.main import app

client = TestClient(app)


def test_description() -> None:
    response: Response = client.get(f"{API_V1_STR}/description")
    assert response.status_code == status.HTTP_200_OK
    try:
        desc = schemas.Desc(**response.json())
        assert desc.name == API_PROJECT_NAME
        assert desc.api_version == __version__
        assert desc.package_version == package_version
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")
