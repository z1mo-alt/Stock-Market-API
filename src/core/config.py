from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str
    stock_api_key: SecretStr
    environment: str = "development"
    debug: bool = False


settings = Settings()