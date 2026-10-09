from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:Welcome1%40@localhost:5432/demo"
    jwt_secret: str = "super-secret-change-me-in-production"
    access_token_minutes: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
