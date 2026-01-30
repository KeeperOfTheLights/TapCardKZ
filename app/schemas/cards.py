"""
Схемы для работы с карточками.

Используются для валидации входящих данных и формирования ответов API.
"""
# Standard Library
import re
from datetime import datetime

# Third-party
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Local
from app.schemas.socials import Out as SocialOut


class Validators(BaseModel):
    """Базовые валидаторы для полей карточки."""
    
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
    """Схема для создания новой карточки."""
    
    name: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        description="Имя владельца карточки",
        json_schema_extra={"example": "John Doe"}
    ) 
    title: str = Field(
        ..., 
        min_length=5, 
        max_length=75, 
        description="Должность или профессия",
        json_schema_extra={"example": "Software Engineer"}
    )
    description: str = Field(
        ..., 
        min_length=10, 
        max_length=255, 
        description="Краткое описание",
        json_schema_extra={"example": "Software Engineer using Python and JavaScript"}
    )
    phone: str = Field(
        ..., 
        description="Номер телефона (формат: 7XXXXXXXXXX)",
        json_schema_extra={"example": "77715229969"}
    )
    email: str = Field(
        ..., 
        description="Email адрес",
        json_schema_extra={"example": "john.doe@example.com"}
    )
    website: str | None = Field(
        None, 
        description="Личный сайт (опционально)",
        json_schema_extra={"example": "https://johndoe.com"}
    )
    city: str = Field(
        ..., 
        min_length=3, 
        max_length=20, 
        description="Город",
        json_schema_extra={"example": "Almaty"}
    )


class Patch(Validators):
    """Схема для частичного обновления карточки (PATCH)."""
    
    name: str | None = Field(
        None, 
        min_length=3, 
        max_length=20, 
        description="Имя владельца карточки",
        json_schema_extra={"example": "Jason Statham"}
    )
    title: str | None = Field(
        None, 
        min_length=5, 
        max_length=75, 
        description="Должность или профессия",
        json_schema_extra={"example": "Actor"}
    )
    description: str | None = Field(
        None, 
        min_length=10, 
        max_length=255, 
        description="Краткое описание",
        json_schema_extra={"example": "Actor from the movie Transporter"}
    )
    phone: str | None = Field(None, description="Номер телефона (формат: 7XXXXXXXXXX)")
    email: str | None = Field(None, description="Email адрес")
    website: str | None = Field(None, description="Личный сайт")
    city: str | None = Field(
        None, 
        min_length=3, 
        max_length=20, 
        description="Город",
        json_schema_extra={"example": "Los Angeles"}
    )


class Base(BaseModel):
    """Базовая схема карточки с полными данными."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Уникальный ID карточки")
    name: str = Field(..., description="Имя владельца")
    title: str = Field(..., description="Должность")
    description: str = Field(..., description="Описание")
    phone: str = Field(..., description="Номер телефона")
    email: str = Field(..., description="Email")
    website: str = Field(..., description="Сайт")
    city: str = Field(..., description="Город")
    is_active: bool = Field(..., description="Активна ли карточка")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")


class Out(Base):
    """Схема ответа при получении карточки."""
    
    socials: list[SocialOut] = Field(default=[], description="Список социальных сетей")
    avatar_link: str | None = Field(None, description="Ссылка на аватар")


class OnCreate(Out):
    """Схема ответа при создании карточки (включает код активации)."""
    
    code: str = Field(..., description="Код активации для редактирования карточки")