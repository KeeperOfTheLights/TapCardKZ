from pydantic import BaseModel, Field


class In(BaseModel):
    code: str = Field(..., min_length=1, example="abc123XYZ")


class Out(BaseModel):
    access_token: str
    token_type: str = "bearer"
    card_id: int

class RegenerateIn(BaseModel):
    card_id: int = Field(..., ge=1)
