from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    MONGODB_DB: str = "restfulapi"
    MONGODB_URI: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
