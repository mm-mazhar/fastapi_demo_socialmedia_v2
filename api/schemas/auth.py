from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserLogin(BaseModel):
    email: str = EmailStr
    password: str = Field(..., min_length=6, max_length=300)


class UserLoginOut(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
