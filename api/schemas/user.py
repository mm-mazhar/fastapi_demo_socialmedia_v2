import datetime
import re
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBaseWithValidator(BaseModel):
    user_created_at: Optional[datetime.datetime] = None
    user_updated_at: Optional[datetime.datetime] = None

    @field_validator("user_created_at", "user_updated_at")
    def parse_user_created_at(cls, value) -> datetime.datetime | Any:
        if value is not None and not isinstance(value, datetime.datetime):
            try:
                return datetime.datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Invalid timestamp format for user_created_at")
        return value


class UserBase(UserBaseWithValidator):
    # id: Optional[int]
    username: str = Field(..., min_length=3, max_length=15)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=300)
    is_active: bool = True
    is_superuser: bool = False

    @field_validator("password")
    def validate_password(cls, v) -> Any:
        if not re.findall("[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.findall("[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.findall("\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.findall("[!@#$%^&*()_+]", v):
            raise ValueError(
                "Password must contain at least one special character (!@#$%^&*()_+)"
            )
        return v

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    # No need to redefine the password here unless you want to change the validation rules
    pass


class UserCreated(UserBaseWithValidator):
    username: str
    email: EmailStr


class UserOut(UserCreated):
    id: int
    is_active: bool
    is_superuser: bool


class UserUpdate(UserCreate):
    is_active: Optional[bool] = True
    
