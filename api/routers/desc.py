from fastapi import APIRouter, status
from loguru import logger

from api import schemas
from api.config import API_PROJECT_NAME, __version__, package_version

desc_router = APIRouter(tags=["Project Description"])


# GET API DESCRIPTION
@desc_router.get(
    "/description", response_model=schemas.Desc, status_code=status.HTTP_200_OK
)
def description() -> schemas.Desc:
    """API Description/Project information.

    Returns:
        schemas.Desc: desc
    """
    desc = schemas.Desc(
        name=API_PROJECT_NAME,
        api_version=__version__,
        package_version=package_version,
    )
    logger.info(f"API Description: {desc}")
    return desc
