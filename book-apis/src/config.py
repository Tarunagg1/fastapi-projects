from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )



Config = Settings()

