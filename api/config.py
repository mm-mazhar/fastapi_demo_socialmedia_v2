import logging
import os
import sys
from types import FrameType
from typing import List, cast

from loguru import logger
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

with open("./api/VERSION") as version_file:
    __version__, API_V1_STR, API_PROJECT_NAME, package_version = map(
        str.strip, version_file.readlines()
    )


class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # logging levels are type int


class Settings(BaseSettings):
    DB_HOSTNAME: str
    # DB_PORT: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASS: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Meta
    logging: LoggingSettings = LoggingSettings()

    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    # e.g: http://localhost,http://localhost:4200,http://localhost:3000
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl | str] = [
        "http://localhost:3000",  # type: ignore
        "http://localhost:8000",  # type: ignore
        "https://localhost:3000",  # type: ignore
        "https://localhost:8001",  # type: ignore
        "*",
    ]

    SERVERS: list[dict[str, str]] = [
        # {
        #     "url": "https://more-socially-fly.ngrok-free.app",
        #     "description": "NGROK server with HTTPS",
        # },
        {
            "url": "https://fastapi-demo-socialmedia-v2.onrender.com",
            "description": "Render server with HTTPS",
        },
        {
            "url": "http://localhost:8012",
            "description": "Local server with HTTPS",
        },
    ]

    class Config:
        env_file: str = ".env"
        case_sensitive = True


# See: https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging  # noqa
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level: str = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame: FrameType = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_app_logging(config: Settings) -> None:
    """Prepare custom logging for our application."""

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Create a log directory if it doesn't exist

    # Format for the log messages
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

    # Configure Loguru logger
    logger.remove()  # Remove default logger
    logger.add(
        sys.stderr, level=config.logging.LOGGING_LEVEL, format=log_format
    )  # CLI sink
    logger.add(
        os.path.join(log_dir, "file_{time}.log"),
        rotation="100 KB",
        retention=1,
        level=config.logging.LOGGING_LEVEL,
        format=log_format,
    )  # File sink

    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger: logging = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]

    # logger.configure(
    #     handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}]
    # )


settings = Settings()
