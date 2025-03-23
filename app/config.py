from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "dev"
    MONGODB_DB: str = "restfulapi"
    MONGODB_URI: str = "mongodb://localhost:27017/"
    JAEGER_ENDPOINT: str = "grpc://localhost:4317"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
