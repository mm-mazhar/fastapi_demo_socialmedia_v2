from fileinput import filename

import pytest

from api import utils

from .config import hashed_password, password


# Test password_hash
@pytest.mark.parametrize("password", password)
def test_password_hash(password: str) -> None:
    """
    Use the pytest.mark.parametrize decorator to parameterize your test.
    Args:
        password (str): each password in the list of passwords
    Returns:
        None
    """
    # Test password_hash
    hashed_password: str = utils.password_hash(password)
    assert (
        hashed_password != password
    ), f"Hashed password should not be the same as the input password for {password}"


# Test verify_password
@pytest.mark.parametrize("plain, hashed", zip(password, hashed_password))
def test_verify_password(plain, hashed) -> None:
    """
    Test that verify_password correctly verifies a password against its hash.
    """
    assert (
        utils.verify_password(plain, hashed) == True
    ), "Password verification failed for {plain} and {hashed}"
