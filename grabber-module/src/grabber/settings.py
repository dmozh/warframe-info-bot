from pydantic import BaseSettings


class Settings(BaseSettings):
    # default
    url = "https://api.warframe.market/v1/items"
    static_url = "https://warframe.market/static/assets/"
    headers = {"Language": "ru"}

    REDIS_HOST = 'redis'
    REDIS_PORT = 6379
    WAIT = 86400


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)