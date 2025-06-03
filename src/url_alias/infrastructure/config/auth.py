from pathlib import Path

from pydantic import BaseModel

from url_alias.infrastructure.config import BASE_DIR


class AuthConfig(BaseModel):
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    PRIVATE_KEY_PATH: Path = BASE_DIR / "jwt_keys" / "jwt_private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "jwt_keys" / "jwt_public.pem"
    ALGORITHM: str = "RS256"
