# apps/app1/src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class App1Settings(BaseSettings):

    app1_specific_setting: str = "app1_default_value"

    model_config = SettingsConfigDict(
        env_file=".env.app1",
        env_prefix="APP1_",
        extra="ignore",
    )


app1_settings = App1Settings()
