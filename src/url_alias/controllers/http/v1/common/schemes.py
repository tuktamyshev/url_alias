from pydantic import AnyHttpUrl, BaseModel, Field


class ExceptionSchema(BaseModel):
    detail: str


class CreateURLSchema(BaseModel):
    expires_in_days: int = Field(gt=0)
    original_url: AnyHttpUrl
