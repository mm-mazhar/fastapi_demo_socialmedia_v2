from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator, Any
from api.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address>:<port>/<dbname>"
# Neon database
SQLALCHEMY_DATABASE_URL: str = (
    f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASS}@{settings.DB_HOSTNAME}/{settings.DB_NAME}?sslmode=require"
)
# Local database
# SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASS}@{settings.DB_HOSTNAME}:{settings.DB_PORT}/{settings.DB_NAME}"

engine: create_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # FOLLOWING ARGUMENT IS ONLY FOR SQLITE DATABASE
    # connect_args={"check_same_thread": False},
    echo=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: declarative_base = declarative_base()


# Dependency
def get_db() -> Generator[sessionmaker, Any, None]:
    """Get database connection.

    Yields:
        SessionLocal: database connection
    """
    db: sessionmaker = SessionLocal()
    try:
        yield db
    finally:
        db.close()
