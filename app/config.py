from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://restfulapi-mongo.default.svc.cluster.local:27017/"
    MONGO_DB: str = "restfulapi"
    ENVIRONMENT: str = "dev"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
