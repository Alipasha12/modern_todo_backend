from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):    
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL: str = Field(default=...,validation_alias="DATABASE_URL")
    SECRET_KEY: str= Field(default=...,validation_alias="SECRET_KEY")
    APP_NAME: str = "FAANG Auth Service"
    APP_V1_STR : str = "/api/v1"
    
    
settings = Settings()

    