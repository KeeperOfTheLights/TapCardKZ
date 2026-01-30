"""
Asset schemas (images).

Used for avatars and social network icons.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core import enums

    
class In(BaseModel):
    """Schema for asset upload."""
    
    card_id: int = Field(
        ..., 
        description="Card ID",
        json_schema_extra={"example": 1}
    )
    type: enums.AssetType = Field(
        ..., 
        description="Asset type (avatar/icon)",
        json_schema_extra={"example": "avatar"}
    )


class Base(BaseModel):
    """Base asset schema."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Asset ID")
    card_id: int = Field(..., description="Card ID")
    type: enums.AssetType = Field(..., description="Asset type")
    file_name: str = Field(..., description="S3 file name")
    created_at: datetime = Field(..., description="Upload date")


class Out(Base):
    """Response schema for asset upload."""
    
    pass