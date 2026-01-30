"""
Asset validators (images).

Check file size and type for uploads.
"""
from fastapi import HTTPException, UploadFile, status

from app.core import config


def validate_image(
    file: UploadFile,
    max_size: int = config.IMAGE_MAX_SIZE,
    allowed_types: list[str] = config.ALLOWED_IMAGE_TYPES
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
