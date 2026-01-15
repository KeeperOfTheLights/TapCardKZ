from pydantic import BaseModel, Field


class CodeIn(BaseModel):
    code: str = Field(..., min_length=1, example="abc123XYZ")


class CodeOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    card_id: int

class CodeRegenerateIn(BaseModel):
    card_id: int
