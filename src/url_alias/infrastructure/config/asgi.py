from pydantic import BaseModel


class ASGIConfig(BaseModel):
    UVICORN_PORT: int
    FASTAPI_DEBUG: bool
    ALLOW_ORIGINS: str
    BACKEND_URL: str
    WEB_DOMAIN: str
