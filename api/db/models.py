from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, ForeignKey,
                        Integer, String, func)
from sqlalchemy.orm import relationship

from .database import Base
from typing import Any

class User(Base):
    """User model/Table.

    Args:
        Base (object): from sqlalchemy.ext.declarative import declarative_base
    """

    __tablename__: str = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    user_created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    user_updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # CheckConstraint to enforce email/password policy
    __table_args__: tuple[CheckConstraint, CheckConstraint, CheckConstraint] = (
        CheckConstraint(
            "LENGTH(username) >= 3 AND LENGTH(username) <= 15 ",
            name="check_username_policy",
        ),
        CheckConstraint(
            "email ~ '^[A-Za-z0-9._%+-]+@(gmail\.com|hotmail\.com)$'"
            "AND LENGTH(email) >= 6 AND LENGTH(email) <= 30 ",
            name="check_valid_email_domain",
        ),
        CheckConstraint(
            "LENGTH(password) >= 6 AND LENGTH(password) <= 300 "
            "AND password ~ '.*[A-Z]+.*' "  # At least one uppercase letter
            "AND password ~ '.*[a-z]+.*' "  # At least one lowercase letter
            "AND password ~ '.*[0-9]+.*' "  # At least one digit
            "AND password ~ '.*[!@#$%^*()_+]+.*'",  # At least one special character
            name="check_password_policy",
        ),
    )


class Posts(Base):
    """Posts model/Table.

    Args:
        Base (object): from sqlalchemy.ext.declarative import declarative_base
    """

    __tablename__: str = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(length=80), nullable=False, unique=False, index=True)
    content = Column(String(length=180), nullable=False, unique=False, index=True)
    published = Column(Boolean, default=True)
    post_created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ratings = Column(Integer, nullable=True, default=None)
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    owner: Any = relationship("User")

    # Enforce character limits
    __table_args__: tuple[CheckConstraint, CheckConstraint] = (
        CheckConstraint(
            "LENGTH(title) >=1 AND LENGTH(title) <= 80", name="title_length_constraint"
        ),
        CheckConstraint(
            "LENGTH(content) >=1 AND LENGTH(content) <= 180",
            name="content_length_constraint",
        ),
    )


class TestSQLALCHEMY(Base):
    """TestSQLALCHEMY model/Table.

    Args:
        Base (object): from sqlalchemy.ext.declarative import declarative_base
    """

    __tablename__: str = "test"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(length=80), nullable=False, unique=False, index=True)
    content = Column(String(length=180), nullable=False, unique=False, index=True)
    published = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ratings = Column(Integer, nullable=True, default=None)

    # Enforce character limits
    __table_args__: tuple[CheckConstraint, CheckConstraint] = (
        CheckConstraint(
            "LENGTH(title) >=1 AND LENGTH(title) <= 80", name="title_length_constraint"
        ),
        CheckConstraint(
            "LENGTH(content) >=1 AND LENGTH(content) <= 180",
            name="content_length_constraint",
        ),
    )
