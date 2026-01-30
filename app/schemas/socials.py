"""
Схемы для работы с социальными сетями карточки.
"""
# Standard Library
from datetime import datetime

# Third-party
from pydantic import BaseModel, ConfigDict, Field

# Local
from app.core import enums


class In(BaseModel):
    """Схема для добавления социальной сети."""
    
    type: enums.SocialType = Field(
        ..., 
        description="Тип социальной сети",
        json_schema_extra={"example": "telegram"}
    )
    url: str = Field(
        ..., 
        description="Ссылка на профиль",
        json_schema_extra={"example": "https://t.me/username"}
    )
    label: str = Field(
        ..., 
        description="Отображаемый текст",
        json_schema_extra={"example": "@username"}
    )


class Patch(BaseModel):
    """Схема для частичного обновления социальной сети."""
    
    type: enums.SocialType | None = Field(None, description="Тип социальной сети")
    url: str | None = Field(None, description="Ссылка на профиль")
    label: str | None = Field(None, description="Отображаемый текст")
    order_id: int | None = Field(None, description="Порядок отображения")
    icon_asset_id: int | None = Field(None, description="ID кастомной иконки")


class Base(BaseModel):
    """Базовая схема социальной сети."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID социальной сети")
    card_id: int = Field(..., description="ID карточки")
    type: enums.SocialType = Field(..., description="Тип социальной сети")
    url: str = Field(..., description="Ссылка на профиль")
    label: str = Field(..., description="Отображаемый текст")
    order_id: int = Field(..., description="Порядок отображения")
    icon_asset_id: int | None = Field(None, description="ID кастомной иконки")
    is_visible: bool = Field(..., description="Видимость")
    created_at: datetime = Field(..., description="Дата создания")


class Out(Base):
    """Схема ответа социальной сети."""
    
    app_icon_link: str | None = Field(None, description="Ссылка на кастомную иконку")