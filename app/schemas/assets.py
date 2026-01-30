"""
Схемы для работы с ассетами (изображениями).

Используются для аватаров и иконок социальных сетей.
"""
# Standard Library
from datetime import datetime

# Third-party
from pydantic import BaseModel, ConfigDict, Field

# Local
from app.core import enums

    
class In(BaseModel):
    """Схема для загрузки ассета."""
    
    card_id: int = Field(
        ..., 
        description="ID карточки",
        json_schema_extra={"example": 1}
    )
    type: enums.AssetType = Field(
        ..., 
        description="Тип ассета (avatar/icon)",
        json_schema_extra={"example": "avatar"}
    )


class Base(BaseModel):
    """Базовая схема ассета."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="ID ассета")
    card_id: int = Field(..., description="ID карточки")
    type: enums.AssetType = Field(..., description="Тип ассета")
    file_name: str = Field(..., description="Имя файла в S3")
    created_at: datetime = Field(..., description="Дата загрузки")


class Out(Base):
    """Схема ответа при загрузке ассета."""
    
    pass