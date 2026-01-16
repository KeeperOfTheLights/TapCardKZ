from pydantic import BaseModel
from app.core import enums
from datetime import datetime
from pydantic import Field  
from pydantic.config import ConfigDict

    
class In(BaseModel):
    card_id: int = Field(..., description="Card ID", example=1)
    type: enums.AssetType = Field(..., description="Asset type", example="avatar")

class Base(BaseModel):
    id: int
    card_id: int
    type: enums.AssetType
    file_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Out(Base):
    pass