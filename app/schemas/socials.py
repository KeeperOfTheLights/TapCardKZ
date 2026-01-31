"""
Social link schemas.
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core import enums


class In(BaseModel):
    """Schema for adding a social link."""
    
    type: enums.SocialType = Field(
        ..., 
        description="Social network type",
        json_schema_extra={"example": "telegram"}
    )
    url: str = Field(
        ..., 
        description="Profile URL",
        json_schema_extra={"example": "https://t.me/username"}
    )
    label: str = Field(
        ..., 
        description="Display text",
        json_schema_extra={"example": "@username"}
    )


class Patch(BaseModel):
    """Schema for partial social link update."""
    
    type: enums.SocialType | None = Field(None, description="Social network type")
    url: str | None = Field(None, description="Profile URL")
    label: str | None = Field(None, description="Display text")
    order_id: int | None = Field(None, description="Display order")
    icon_asset_id: int | None = Field(None, description="Custom icon ID")


class Base(BaseModel):
    """Base social link schema."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Social link ID")
    card_id: int = Field(..., description="Card ID")
    type: enums.SocialType = Field(..., description="Social network type")
    url: str = Field(..., description="Profile URL")
    label: str = Field(..., description="Display text")
    order_id: int = Field(..., description="Display order")
    icon_asset_id: int | None = Field(None, description="Custom icon ID")
    is_visible: bool = Field(..., description="Visibility")
    created_at: datetime = Field(..., description="Creation date")


class Out(Base):
    """Social link response schema."""
    
    app_icon_link: str | None = Field(None, description="Custom icon URL")