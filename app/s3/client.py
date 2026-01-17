from aioboto3.session import Session
from contextlib import asynccontextmanager
from app.core.config import config
from app.core.logger import logger

class S3Client:
    def __init__(
        self, 
        aws_access_key_id: str, 
        aws_secret_access_key: str, 
        endpoint_url: str, 
        bucket_name: str
    ):
        self.config: dict = {
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
            "endpoint_url": endpoint_url
        }
        self.bucket_name: str = bucket_name
        self.session: Session = Session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_obj, object_name: str) -> None:
        async with self.get_client() as client:
            await client.upload_fileobj(file_obj, self.bucket_name, object_name)
        logger.info(f"File {object_name} uploaded to S3")

    async def get_object_url(self, object_name: str) -> str:
        #TODO: REDIS CASH
        async with self.get_client() as client:
            url: str = await client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": object_name},
                ExpiresIn=config.IMAGE_EXPIRE_TIME,
            )
            logger.info(f"URL for file {object_name} generated")
            return url

    async def delete_asset(self, file_name: str) -> None:
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=file_name)
        logger.info(f"File {file_name} deleted")
        
          
