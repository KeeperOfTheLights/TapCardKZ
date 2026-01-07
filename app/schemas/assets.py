from pydantic import BaseModel
from app.core.models.asset import AssetType
from datetime import datetime

class AssetIn(BaseModel):
    card_id: int
    type: AssetType

class AssetOut(BaseModel):
    id: int
    card_id: int
    type: AssetType
    file_name: str
    created_at: datetime