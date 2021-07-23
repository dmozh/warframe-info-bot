# временное решение
from pydantic import BaseSettings


class Settings(BaseSettings):
    token = ''
    bot = 'WarframeBot-info'
    id = 686219829337784330
    prefix = '$'

    REDIS_HOST = '192.168.0.21'
    REDIS_PORT = 6379

    WF_MARKET_API_HOST = "https://api.warframe.market/v1"
    WF_MARKET_HEADERS = {"platform": 'pc'}

    TIMER = 600


settings = Settings()