from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str    
    DB_HOST: str
    DB_PORT: int

    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_DOMAIN: str
    BUCKET_NAME: str

    ALLOWED_IMAGE_TYPES: list[str]
    IMAGE_MAX_SIZE: int
    IMAGE_EXPIRE_TIME: int

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    LOG_DIR: str

    S3_AVATAR_TEMPLATE: str
    S3_ICON_TEMPLATE: str

    CODE_LEN: int

    ADMIN_SECRET: str
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

config: Config = Config()