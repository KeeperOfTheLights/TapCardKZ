"""
Activation code schemas.

Codes are used for card owner authentication.
"""
from pydantic import BaseModel, Field


class In(BaseModel):
    """Schema for code redemption (getting token)."""
    
    code: str = Field(
        ..., 
        min_length=1, 
        description="Activation code for login",
        json_schema_extra={"example": "abc123XYZ"}
    )


class Out(BaseModel):
    """Response schema for successful code redemption."""
    
    access_token: str = Field(..., description="JWT token for authorization")
    token_type: str = Field(default="bearer", description="Token type")
    card_id: int = Field(..., description="Card ID linked to the code")


class RegenerateIn(BaseModel):
    """Request schema for code regeneration (admin only)."""
    
    card_id: int = Field(
        ..., 
        ge=1, 
        description="Card ID to regenerate code for",
        json_schema_extra={"example": 1}
    )


class RegenerateOut(BaseModel):
    """Response schema for code regeneration."""
    
    card_id: int = Field(..., description="Card ID")
    code: str = Field(..., description="New activation code")
