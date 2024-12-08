from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

# import oauth2
from api import oauth2, schemas, utils
from api.db import models
from api.db.database import get_db

# Prefix for all "Users" endpoints
preFix_user = "/users"

user_router = APIRouter(prefix=preFix_user, tags=["Users"])


# CREATE USER/SUPERUSER
@user_router.post(
    "/create-user",
    response_model=schemas.UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
) -> schemas.UserOut:
    """Create a user/superuser.
    Args:
        user (schemas.UserCreate): User data.
        db (Session): Database session. Defaults to Depends(get_db).
    Raises:
        HTTPException: 422 Unprocessable Entity for creation failure.
    Returns:
        schemas.UserCreate: New user data.
    """

    # print("Current User: ", current_user)
    # Hash the password | user.password is a plain text password
    hashed_password: str = utils.password_hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Failed to create user",
        )
    # Check if the username or email already exists
    existing_user: Any = (
        db.query(models.User)
        .filter(
            (models.User.username == user.username) | (models.User.email == user.email)
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username: {user.username} or email: {user.email} already exists",
        )
    # Add the new user to the session
    db.add(new_user)
    # Commit the changes to the database
    db.commit()
    # Refresh the object to get the updated values from the database
    db.refresh(new_user)
    return new_user


# GET USER/s
@user_router.get(
    "/get",
    response_model=list[schemas.UserOut],
    status_code=status.HTTP_200_OK,
)
async def get_user_by_username(
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
    limit: int = 100,
    skip: int = 0,
    search: Optional[str] = "",
) -> list[schemas.UserOut]:
    """GET USER/s
    Args:
    db (Session): Session.
    current_user (dict): AuthUser.
    limit, skip (int): No. of users to return/skip, default 100 0.
    search (Opt[str]): Query, default Null.
    Raises:
        HTTPException: 404 Not Found.
    Returns:
        List[schemas.UserOut]: User data.
    """
    # print("Current User: ", current_user)
    if current_user["is_superuser"]:
        if search:
            users: Any = (
                db.query(models.User)
                .filter(models.User.username.ilike(f"%{search}%"))
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            users = db.query(models.User).offset(skip).limit(limit).all()
        return users
    else:
        users = (
            db.query(models.User)
            .filter(models.User.username == current_user["username"])
            .all()
        )
        return users


# UPDATE USER BY USERNAME
@user_router.put(
    "/update/{userName}",
    response_model=schemas.UserCreated,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_user_by_username(
    updated_user: schemas.UserUpdate,
    # username: str,
    userName: str = Path(..., description="The username to update"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
) -> schemas.UserCreated:
    """UPDATE USER BY USERNAME (PUT METHOD)
    Args:
        username: str
        user: schemas.UserCreate
        db: Session, Depends(get_db).
        current_user (dict): Depends(oauth2.get_current_user).
    Raises:
        HTTPException: 404 Not Found.
    Returns:
        schemas.UserCreated
    """
    print("Current User: ", current_user)
    # Check if the user exists
    user: Any = db.query(models.User).filter(models.User.username == userName).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username={userName} not found",
        )
    if user.username == current_user["username"] or current_user["is_superuser"]:
        hashed_password: str = utils.password_hash(updated_user.password)
        updated_user.password = hashed_password
        print("*" * 50)
        print("updated_user: ", updated_user)
        print("user: ", updated_user.password)
        print("*" * 50)
        # user = models.User(**user.model_dump())
        # print("Updated User: ", updated_user.model_dump(exclude_unset=True)
        # Update the user fields with the new values
        for field, value in updated_user.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        # Commit the changes to the database
        db.commit()
        # Refresh the user object to get the updated values from the database
        db.refresh(user)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Loggein in as User: '{current_user['username']}' | Either not a superuser or Not Authorized",
        )


# DELETE USER BY ID
@user_router.delete(
    "/delete/id/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    """DELETE USER BY ID
    Args:
        id (int): user id
        db (Session): Session, Depends(get_db).
        current_user (dict): Depends(oauth2.get_current_user).
    Raises:
        HTTPException: 404 Not Found.
    Returns:
        schemas.ResponseBase
    """
    # print("Current User: ", current_user)
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id={id} not found"
        )
    if user.username == current_user["username"] or current_user["is_superuser"]:
        user_query.delete(synchronize_session=False)
        db.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Loggein in as User: '{current_user['username']}' | Either not a superuser or Not Authorized",
        )


# DELETE USER BY USERNAME
@user_router.delete(
    "/delete/{username}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_by_username(
    username: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    """DELETE USER BY USERNAME
    Args:
        username: str
        db (Session): Depends(get_db)
        current_user (dict): Depends(oauth2.get_current_user)
    Raises:
        HTTPException: 404 Not Found.
    Returns:
        schemas.ResponseBase
    """
    # print("Current User: ", current_user)
    user_query = db.query(models.User).filter(models.User.username == username)
    user = user_query.first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username={username} not found",
        )
    if user.username == current_user["username"] or current_user["is_superuser"]:
        user_query.delete(synchronize_session=False)
        db.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Loggein in as User: '{current_user['username']}' | Either not a superuser or Not Authorized",
        )
