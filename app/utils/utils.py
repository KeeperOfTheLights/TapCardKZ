"""
Утилиты общего назначения.
"""
# Standard Library
from typing import Type

# Third-party
from pydantic import BaseModel


def build_schema(
    schema_class: Type[BaseModel], 
    *models: BaseModel, 
    **extra_fields
) -> BaseModel:
    """
    Собрать схему из нескольких моделей и дополнительных полей.
    
    Args:
        schema_class: Класс схемы для создания
        *models: Модели для объединения
        **extra_fields: Дополнительные поля
        
    Returns:
        BaseModel: Экземпляр schema_class
    """
    data = {}
    for model in models:
        data.update(model.model_dump())
    data.update(extra_fields)
    return schema_class(**data)