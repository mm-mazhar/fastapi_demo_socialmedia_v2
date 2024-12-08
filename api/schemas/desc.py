from pydantic import BaseModel


class Desc(BaseModel):
    name: str
    api_version: str
    package_version: str
