"""
General utilities.
"""
from pydantic import BaseModel


def build_schema(schema_class: type[BaseModel], *models, **extra_fields) -> BaseModel:
    """
    Build schema from multiple models and additional fields.
    
    Args:
        schema_class: Schema class to create
        *models: Models to combine
        **extra_fields: Additional fields
        
    Returns:
        BaseModel: Instance of schema_class
    """
    combined = {}
    for model in models:
        if hasattr(model, "__dict__"):
            combined.update({
                k: v for k, v in model.__dict__.items() 
                if not k.startswith("_")
            })
    combined.update(extra_fields)
    return schema_class(**combined)