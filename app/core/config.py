from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database settings
    SQLALCHEMY_DATABASE_URI: str = Field(..., env="DATABASE_URL")

    # Application settings
    APP_NAME: str = "FastAPI Blogs Backend"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Token expiration time

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instantiate the settings object
settings = Settings()
