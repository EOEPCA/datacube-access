from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GDC_")

    id: str
    title: str
    description: str
    data_backend: str  # Currently supporting stac api


@lru_cache
def get_config():
    return Config()
