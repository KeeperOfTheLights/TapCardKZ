"""
Card schemas.

Used for validating input data and formatting API responses.
"""
import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.socials import Out as SocialOut


class Validators(BaseModel):
    """Base validators for card fields."""
    
    phone: str | None = None
    email: str | None = None
    website: str | None = None

    @field_validator("phone")
    def validate_phone(cls, v: str) -> str:
        if v is None:
            return v
        if not v.startswith("7"):
            raise ValueError("Phone number must start with 7")
        if len(v) != 11:
            raise ValueError("Phone number must be 11 characters long")
        if not v[1:].isdigit():
            raise ValueError("Phone number must contain only digits")
        return v
    
    @field_validator("email")
    def validate_email(cls, v: str) -> str:
        if v is None:
            return v
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", v):
            raise ValueError("Invalid email format")
        return v
    
    @field_validator("website")
    def validate_website(cls, v: str) -> str:
        if v is None:
            return v
        if not v.startswith("http://") and not v.startswith("https://"):
            raise ValueError("Website must start with http:// or https://")
        return v


class In(Validators):
    """Schema for creating a new card."""
    
    name: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        description="Card owner name",
        json_schema_extra={"example": "John Doe"}
    ) 
    title: str = Field(
        ..., 
        min_length=5, 
        max_length=75, 
        description="Job title or profession",
        json_schema_extra={"example": "Software Engineer"}
    )
    description: str = Field(
        ..., 
        min_length=10, 
        max_length=255, 
        description="Brief description",
        json_schema_extra={"example": "Software Engineer using Python and JavaScript"}
    )
    phone: str = Field(
        ..., 
        description="Phone number (format: 7XXXXXXXXXX)",
        json_schema_extra={"example": "77715229969"}
    )
    email: str = Field(
        ..., 
        description="Email address",
        json_schema_extra={"example": "john.doe@example.com"}
    )
    website: str | None = Field(
        None, 
        description="Personal website (optional)",
        json_schema_extra={"example": "https://johndoe.com"}
    )
    city: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        description="City",
        json_schema_extra={"example": "Almaty"}
    )


class Patch(Validators):
    """Schema for partial card update (PATCH)."""
    
    name: str | None = Field(
        None, 
        min_length=3, 
        max_length=20, 
        description="Card owner name",
        json_schema_extra={"example": "Jason Statham"}
    )
    title: str | None = Field(
        None, 
        min_length=5, 
        max_length=75, 
        description="Job title or profession",
        json_schema_extra={"example": "Actor"}
    )
    description: str | None = Field(
        None, 
        min_length=10, 
        max_length=255, 
        description="Brief description",
        json_schema_extra={"example": "Actor from the movie Transporter"}
    )
    phone: str | None = Field(None, description="Phone number (format: 7XXXXXXXXXX)")
    email: str | None = Field(None, description="Email address")
    website: str | None = Field(None, description="Personal website")
    city: str | None = Field(
        None, 
        min_length=3, 
        max_length=20, 
        description="City",
        json_schema_extra={"example": "Los Angeles"}
    )


class Base(BaseModel):
    """Base card schema with full data."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Unique card ID")
    name: str = Field(..., description="Owner name")
    title: str = Field(..., description="Job title")
    description: str = Field(..., description="Description")
    phone: str = Field(..., description="Phone number")
    email: str = Field(..., description="Email")
    website: str = Field(..., description="Website")
    city: str = Field(..., description="City")
    is_active: bool = Field(..., description="Whether card is active")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")


class Out(Base):
    """Response schema for getting a card."""
    
    socials: list[SocialOut] = Field(default=[], description="List of social links")
    avatar_link: str | None = Field(None, description="Avatar URL")


class OnCreate(Out):
    """Response schema when creating a card (includes activation code)."""
    
    code: str = Field(..., description="Activation code for card editing")