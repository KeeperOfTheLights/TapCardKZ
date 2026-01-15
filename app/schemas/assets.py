from pydantic import BaseModel
from app.core.models.asset import AssetType
from datetime import datetime
from pydantic import Field  
from pydantic.config import ConfigDict

class LogoLinksOut(BaseModel):
    order_id: int
    link: str
    
class AssetIn(BaseModel):
    card_id: int = Field(..., description="Card ID", example=1)
    type: AssetType = Field(..., description="Asset type", example="avatar")

class AssetBase(BaseModel):
    id: int
    card_id: int
    type: AssetType
    file_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AssetOut(AssetBase):
    pass