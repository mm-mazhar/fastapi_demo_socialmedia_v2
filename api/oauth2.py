from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# import schemas
from api import schemas
from api.config import API_V1_STR, settings
from api.db import models
from api.db.database import get_db

# Move the first character to the end
API_V1_STR: str = API_V1_STR[1:] + API_V1_STR[0]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_V1_STR}login")

# SECRET KEY
SECRET_KEY: str = settings.SECRET_KEY
# ALGORITHM
ALGORITHM: str = settings.ALGORITHM
# EXPIRATION TIME
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode: dict = data.copy()
    if expires_delta:
        expire: datetime = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        username: str = payload.get("username")
        is_active: bool = payload.get("is_active")
        is_superuser: bool = payload.get("is_superuser")

        if (
            (id is None)
            or (username is None)
            or (is_active is None)
            or (is_superuser is None)
        ):
            raise credentials_exception
        token_data = schemas.TokenData(
            id=id, username=username, is_active=is_active, is_superuser=is_superuser
        )
    except JWTError:
        raise credentials_exception

    # print("Token Data: ", token_data)
    return token_data


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
)-> dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    # print("Token: ", token)
    user: Any = db.query(models.User).filter(models.User.id == token.id).first()
    user = {
        "id": user.id,
        "username": user.username,
        "is_active": user.is_active,
        "is_superuser": user.is_superuser,
    }
    # print("User: ", user)
    return user
