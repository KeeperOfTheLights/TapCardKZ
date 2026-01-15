import re
from datetime import datetime
from app.schemas.socials import SocialOut
from pydantic import BaseModel, field_validator, Field, ConfigDict
from app.schemas.socials import BaseSocial, SocialPatch


class CardValidators(BaseModel):
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

class CardIn(CardValidators):
    name: str = Field(..., min_length=3, max_length=20, example="John Doe") 
    title: str = Field(..., min_length=5, max_length=75, example="Engineer")
    description: str = Field(..., min_length=10, max_length=255, example="Software Engineer using Python and JavaScript")
    phone: str = Field(..., example="77715229969")
    email: str = Field(..., example="john.doe@example.com")
    website: str | None = Field(None, example="https://johndoe.com")
    city: str = Field(..., min_length=3, max_length=20, example="Almaty")

class CardPatch(CardValidators):
    name: str | None = Field(None, min_length=3, max_length=20, example="Jason Statham")
    title: str | None = Field(None, min_length=5, max_length=75, example="Actor")
    description: str | None = Field(None, min_length=10, max_length=255, example="Actor from the movie Transporter")
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    city: str | None = Field(None, min_length=3, max_length=20, example="Los Angeles")

class CardBase(BaseModel):
    id: int 
    name: str
    title: str
    description: str    
    phone: str
    email: str
    website: str
    city: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class CardOut(CardBase):
    socials: list[SocialOut]
    avatar_link: str | None

class CardOutOnCreate(CardOut):
    code: str