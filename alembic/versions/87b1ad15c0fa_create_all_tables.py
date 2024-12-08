"""Create All Tables

Revision ID: 87b1ad15c0fa
Revises: 18ac241fd016
Create Date: 2024-02-14 23:21:52.514332

"""

from datetime import datetime
from typing import Any, Sequence, Union

import sqlalchemy as sa
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.sql import column, table

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "87b1ad15c0fa"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Use Python's datetime.now() to get the current time
current_time: datetime = datetime.now()


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "user_created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "user_updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="false"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
        sa.CheckConstraint(
            "LENGTH(username) >= 3 AND LENGTH(username) <= 15 ",
            name="check_username_policy",
        ),
        sa.CheckConstraint(
            "email ~ '^[A-Za-z0-9._%+-]+@(gmail.com|hotmail.com)$' AND LENGTH(email) >= 6 AND LENGTH(email) <= 30 ",
            name="check_valid_email_domain",
        ),
        sa.CheckConstraint(
            "LENGTH(password) >= 6 AND LENGTH(password) <= 300 AND password ~ '.*[A-Z]+.*' AND password ~ '.*[a-z]+.*' AND password ~ '.*[0-9]+.*' AND password ~ '.*[!@#$%^*()_+]+.*'",
            name="check_password_policy",
        ),
    )

    # Insert values into the users table
    users_table: Any = table(
        "users",
        column("username", String),
        column("email", String),
        column("password", String),
        column("is_active", Boolean),
        column("is_superuser", Boolean),
        column("user_created_at", DateTime),
        column("user_updated_at", DateTime),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "username": "admin",
                "email": "admin@gmail.com",
                "password": "$2b$12$NlqpBJ7Ml/SSBxCcy5o.z.V1vOX7Q0Qlxjw1y12VrsHmVDEasOdiK",
                "is_active": True,
                "is_superuser": True,
                # "user_created_at": current_time,
                # "user_updated_at": current_time,
            },
            {
                "username": "user",
                "email": "user@hotmail.com",
                "password": "$2b$12$NlqpBJ7Ml/SSBxCcy5o.z.V1vOX7Q0Qlxjw1y12VrsHmVDEasOdiK",
                "is_active": True,
                "is_superuser": False,
                # "user_created_at": current_time,
                # "user_updated_at": current_time,
            },
        ],
    )

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.Column("content", sa.String(length=180), nullable=False),
        sa.Column("published", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "post_created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("ratings", sa.Integer(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], ondelete="CASCADE", onupdate="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "LENGTH(title) >=1 AND LENGTH(title) <= 80", name="title_length_constraint"
        ),
        sa.CheckConstraint(
            "LENGTH(content) >=1 AND LENGTH(content) <= 180",
            name="content_length_constraint",
        ),
    )

    # Insert values into the posts table
    posts_table: Any = table(
        "posts",
        column("title", String),
        column("content", String),
        column("published", Boolean),
        column("post_created_at", DateTime),
        column("ratings", Integer),
        column(
            "owner_id", Integer
        ),  # Assuming this is a foreign key to the users table
    )

    op.bulk_insert(
        posts_table,
        [
            {
                "title": "Favorite Food",
                "content": "Pizza",
                "published": True,
                # "post_created_at": current_time,
                "ratings": 5,
                "owner_id": 1,
            },
            {
                "title": "Favorite Movie",
                "content": "X-Men",
                "published": True,
                # "post_created_at": current_time,
                "ratings": 4,
                "owner_id": 2,
            },
            # Add more posts as needed
        ],
    )

    op.create_table(
        "test",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.Column("content", sa.String(length=180), nullable=False),
        sa.Column("published", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("ratings", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.CheckConstraint(
            "LENGTH(title) >=1 AND LENGTH(title) <= 80", name="title_length_constraint"
        ),
        sa.CheckConstraint(
            "LENGTH(content) >=1 AND LENGTH(content) <= 180",
            name="content_length_constraint",
        ),
    )


def downgrade() -> None:
    op.drop_table("test")
    op.drop_table("posts")
    op.drop_table("users")
