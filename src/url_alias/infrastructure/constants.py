import enum


class JWTTokenType(enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"
