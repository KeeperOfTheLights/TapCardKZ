from pydantic import BaseModel, Field


class CodeRedeemIn(BaseModel):
    code: str = Field(..., min_length=1, example="abc123XYZ")


class CodeRedeemOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    card_id: int  # We return this so user knows which card they can edit


class RegenerateCodeIn(BaseModel):
    card_id: int = Field(..., ge=1, example=1)

class CodeRegenerateOut(BaseModel):
    code: str
    card_id: int
