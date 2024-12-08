from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# import oauth2
from api import oauth2, schemas
from api.db import models
from api.db.database import get_db

preFix_post = "/posts"

post_router = APIRouter(prefix=preFix_post, tags=["Posts"])


# GET ALL POSTS
@post_router.get(
    "/get",
    response_model=list[schemas.ResponseBase],
    status_code=status.HTTP_200_OK,
)
async def get_posts(
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
    limit: int = 100,
    skip: int = 0,
    search: Optional[str] = "",
) -> list[schemas.ResponseBase]:
    """GET ALL POSTS
    Args:
        db: Depends(get_db)
        current_user (dict): Depends(oauth2.get_current_user)
        limit, skip (int): Defaults to 100 & 0
        search (Optional[str], optional): Search str in title col. Defaults to ""
    Returns:
        list[schemas.ResponseBase]
    """
    # print("Current User: ", current_user["id"])
    if current_user["is_superuser"]:
        all_posts: Any = (
            db.query(models.Posts)
            .filter(models.Posts.title.contains(search))
            .limit(limit)
            .offset(skip)
            .all()
        )
        return all_posts
    else:
        all_posts = (
            db.query(models.Posts)
            .filter(models.Posts.owner_id == current_user["id"])
            .filter(models.Posts.title.contains(search))
            .limit(limit)
            .offset(skip)
            .all()
        )
        if len(all_posts) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No posts found for user with owner_id={current_user['id']} or user is not a superuser",
            )
        return all_posts


# CREATE A POST
@post_router.post(
    "/create",
    response_model=schemas.ResponseBase,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
) -> schemas.ResponseBase:
    """CREATE A POST
    Args:
        post: schemas.CreatePost
        db: Session, Defaults to Depends(get_db)
        current_user (dict): Depends(oauth2.get_current_user)
    Raises:
        HTTPException: 422 Unprocessable Entity
    Returns:
        schemas.ResponseBase
    """
    # print("Incoming Post: ", post.model_dump())
    # new_post = models.Posts(
    #     title=post.title, content=post.content, published=post.published
    # )
    # Update
    # Create a new instance of the SQLAlchemy model with owner_id set
    new_post = models.Posts(
        title=post.title,
        content=post.content,
        published=post.published,
        owner_id=int(current_user["id"]),
    )
    if not new_post:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Failed to create post",
        )
    # Add the new post to the session
    db.add(new_post)
    # Commit the changes to the database
    db.commit()
    # Refresh the object to get the updated values from the database
    db.refresh(new_post)
    return new_post


# GET A POST BY ID
@post_router.get(
    "/id/{id}", response_model=schemas.ResponseBase, status_code=status.HTTP_200_OK
)
async def get_post_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
) -> schemas.ResponseBase:
    """GET A POST BY ID
    Args:
        id (int): id
        db: Session, Defaults to Depends(get_db)
        current_user (dict): Depends(oauth2.get_current_user)
    Raises:
        HTTPException: 404 Not Found
    Returns:
        schemas.ResponseBase
    """
    post: Any = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id={id} not found or current user is not the owner of the post with id={id}",
        )
    if post.owner_id == current_user["id"] or current_user["is_superuser"]:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Either Post with id={id} is not owned by user with owner_id={current_user['id']} or user is not a superuser",
        )


# GET LATEST POST
@post_router.get(
    "/latest", response_model=schemas.ResponseBase, status_code=status.HTTP_200_OK
)
async def get_post_latest(
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
) -> schemas.ResponseBase:
    """GET LATEST POST
    Args:
        db: Session, Depends(get_db)
        current_user (dict): Depends(oauth2.get_current_user)
    Raises:
        HTTPException: 404 Not Found.
    Returns:
        schemas.ResponseBase
    """
    latest_post: Any = db.query(models.Posts).order_by(models.Posts.id.desc()).first()
    if not latest_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No post found"
        )
    if latest_post.owner_id == current_user["id"] or current_user["is_superuser"]:
        return latest_post
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Either Latest Post is not owned by user with ower_id={current_user['id']} or user is not a superuser",
        )


# DELETE A POST BY ID
@post_router.delete(
    "/delete/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
):
    """DELETE A POST BY ID
    Args:
        id (int): id
        db: Session, Depends(get_db).
        current_user (dict): Depends(oauth2.get_current_user).
    Raises:
        HTTPException: 404 Not Found.
    Returns:
        Status: 204 No Content.
    """
    post_query: Any = db.query(models.Posts).filter(models.Posts.id == id)

    post: Any = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} not found"
        )
    if post.owner_id == current_user["id"] or current_user["is_superuser"]:
        post_query.delete(synchronize_session=False)
        db.commit()
        return HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Either Post with id={id} is not owned by user with owner_id={current_user['id']} or user is not a superuser",
        )


# UPDATE A POST BY ID (USING PUT METHOD -> REPLACE THE ALL ENTRIES)
@post_router.put(
    "/update/{id}",
    response_model=schemas.ResponseBase,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_post_by_id(
    id: int,
    updated_post: schemas.UpdatePost,
    db: Session = Depends(get_db),
    current_user: dict = Depends(oauth2.get_current_user),
) -> schemas.ResponseBase:
    """UPDATE A POST BY ID (PUT METHOD)
    Args:
        id (int): id
        updated_post: schemas.UpdatePost
        db: Session,Depends(get_db).
        current_user (dict): Depends(oauth2.get_current_user).
    Raises:
        HTTPException: 404 Not Found.
    Returns:
        schemas.ResponseBase
    """
    post: Any = db.query(models.Posts).filter(models.Posts.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id={id} not found"
        )

    if post.owner_id == current_user["id"] or current_user["is_superuser"]:
        # # Convert Pydantic model to a dictionary using jsonable_encoder
        # updated_post_data = jsonable_encoder(updated_post)
        # # Update the post with the new values
        # for field, value in updated_post_data.items():
        #     setattr(post, field, value)
        # Update the post with the new values
        for field in updated_post.model_dump(exclude_unset=True):
            setattr(post, field, getattr(updated_post, field))
        # Commit the changes to the database
        db.commit()
        # Refresh the object to get the updated values from the database
        db.refresh(post)
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Either Post with id={id} is not owned by user with owner_id={current_user['id']} or user is not a superuser",
        )
