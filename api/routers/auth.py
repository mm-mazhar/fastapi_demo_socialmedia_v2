# import oauth2
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# import schemas
from api import oauth2, schemas
from api.db import models
from api.db.database import get_db
from api import utils

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/login", response_model=schemas.Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Login Route: Generates access token for user.
    Args:
        user_credentials (OAuth2PasswordRequestForm): User login data.
        db (Session): Database session.
    Raises:
        HTTPException: 403 Forbidden for invalid credentials.
    Returns:
        dict: Access token and type.
    """

    user: Any = (
        db.query(models.User)
        .filter(
            models.User.email == user_credentials.username
        )  # username is email because of SWAGGER UI bug in OAuth2PasswordRequestForm
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    access_token: str = oauth2.create_access_token(
        data={
            "user_id": user.id,
            "username": user.username,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
        }
    )

    return {"access_token": access_token, "token_type": "bearer"}
