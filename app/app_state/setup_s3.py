from fastapi import FastAPI

from app.s3.client import S3Client
from app.core.config import config
from app.core.logger import logger

async def setup_s3(app: FastAPI) -> None:
    logger.info("Initializing S3 client...")
    app.state.s3_client = S3Client(
        aws_access_key_id=config.S3_ACCESS_KEY,
        aws_secret_access_key=config.S3_SECRET_KEY,
        endpoint_url=config.S3_DOMAIN,
        bucket_name=config.BUCKET_NAME,
    )


async def cleanup_s3(app: FastAPI) -> None:
    logger.info("S3 client disposed")