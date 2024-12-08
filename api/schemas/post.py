import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field, field_validator

from .user import UserCreated


class ResponseBase(BaseModel):
    id: Optional[int]
    title: str = Field(..., min_length=1, max_length=80)
    content: str = Field(..., min_length=1, max_length=180)
    published: bool
    post_created_at: Optional[datetime.datetime]
    ratings: Optional[int] = None
    owner_id: int
    owner: UserCreated  # imported from users.py in schemas

    @field_validator("post_created_at")
    def parse_post_created_at(cls, value) -> datetime.datetime | Any:
        if value is not None and not isinstance(value, datetime.datetime):
            try:
                # Assuming the input is a string
                return datetime.datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid timestamp format for post_created_at")
        return value

    class Config:
        from_attributes = True


class ResponseBaseExtended(ResponseBase):
    pass


class CreatePost(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)
    content: str = Field(..., min_length=1, max_length=180)
    published: bool = True
    # owner_id: int


class UpdatePost(CreatePost):
    published: bool
    # owner_id: Optional[int]


class PostCreated(BaseModel):
    id: int
    title: str = Field(..., min_length=1, max_length=80)
    content: str = Field(..., min_length=1, max_length=180)
    post_created_at: Optional[datetime.datetime]

    @field_validator("post_created_at")
    def parse_post_created_at(cls, value)-> datetime.datetime | Any:
        if value is not None and not isinstance(value, datetime.datetime):
            try:
                # Assuming the input is a string
                return datetime.datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid timestamp format for post_created_at")
        return value

    class Config:
        from_attributes = True


class DeletePost(BaseModel):
    id: int
    msg: str = "Post deleted successfully"
