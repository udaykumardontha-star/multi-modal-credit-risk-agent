import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str | None = None
    MODEL_PROVIDER: str = "openai"
    VISION_MODEL: str = "gpt-4o"
    REDIS_URL: str = "redis://localhost:6379/0"
    MAX_FILE_SIZE_MB: int = 20
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".png", ".jpg", ".jpeg", ".webp", ".csv", ".xlsx"]
    OUTPUT_DIR: str = "/tmp/outputs"
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

# Ensure OUTPUT_DIR exists
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
