"""
Asset validators (images).

Check file size and type for uploads.
"""
from fastapi import HTTPException, UploadFile, status

from app.core.config import config


async def validate_image(
    file: UploadFile,
    max_size: int = None,
    allowed_types: list[str] = None
) -> None:
    """
    Validate image file by size and type.
    
    Args:
        file: Uploaded file
        max_size: Maximum size in bytes (default from config)
        allowed_types: Allowed MIME types (default from config)
        
    Raises:
        HTTPException: 413 if file too large
        HTTPException: 400 if file type not allowed
    """
    if max_size is None:
        max_size = config.IMAGE_MAX_SIZE
    if allowed_types is None:
        allowed_types = config.ALLOWED_IMAGE_TYPES
    
    # Проверяем тип файла
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not allowed file type, allowed types: {', '.join(allowed_types)}"
        )
    
    # Проверяем размер файла
    # file.size может быть None, поэтому читаем файл для проверки размера
    if file.size is not None and file.size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large, maximum size is {max_size / 1024 / 1024:.1f}MB"
        )
    
    # Если file.size == None, проверяем размер путем чтения файла
    if file.size is None:
        contents = await file.read()
        if len(contents) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large, maximum size is {max_size / 1024 / 1024:.1f}MB"
            )
        # Возвращаем указатель в начало файла для дальнейшей обработки
        await file.seek(0)

