"""
Схемы для работы с кодами активации.

Коды используются для аутентификации владельца карточки.
"""
# Third-party
from pydantic import BaseModel, Field


class In(BaseModel):
    """Схема для активации кода (получение токена)."""
    
    code: str = Field(
        ..., 
        min_length=1, 
        description="Код активации для входа",
        json_schema_extra={"example": "abc123XYZ"}
    )


class Out(BaseModel):
    """Схема ответа при успешной активации кода."""
    
    access_token: str = Field(..., description="JWT токен для авторизации")
    token_type: str = Field(default="bearer", description="Тип токена")
    card_id: int = Field(..., description="ID карточки, к которой привязан код")


class RegenerateIn(BaseModel):
    """Схема запроса на регенерацию кода (только для админов)."""
    
    card_id: int = Field(
        ..., 
        ge=1, 
        description="ID карточки для регенерации кода",
        json_schema_extra={"example": 1}
    )


class RegenerateOut(BaseModel):
    """Схема ответа при регенерации кода."""
    
    card_id: int = Field(..., description="ID карточки")
    code: str = Field(..., description="Новый код активации")
