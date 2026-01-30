"""
Валидаторы для ассетов (изображений).

Проверяют размер и тип загружаемых файлов.
"""
# Third-party
from fastapi import HTTPException, UploadFile, status

# Local
from app.core import config


def validate_image(
    file: UploadFile,
    max_size: int = config.IMAGE_MAX_SIZE,
    allowed_types: list[str] = config.ALLOWED_IMAGE_TYPES
) -> None:
    """
    Валидация файла изображения по размеру и типу.
    
    Args:
        file: Загружаемый файл
        max_size: Максимальный размер в байтах (по умолчанию из конфига)
        allowed_types: Разрешённые MIME-типы (по умолчанию из конфига)
        
    Raises:
        HTTPException: 413 если файл слишком большой
        HTTPException: 400 если тип файла не разрешён
    """
    if file.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Too large file, it must be less than 5MB"
        )
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not allowed file type, allowed types: {', '.join(allowed_types)}"
        )
