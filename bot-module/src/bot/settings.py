from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    token = os.getenv("token")
    bot = 'WarframeBot-info'
    id = 686219829337784330
    prefix = '$'

    REDIS_HOST = 'redis'
    REDIS_PORT = 6379

    WF_MARKET_API_HOST = "https://api.warframe.market/v1"
    WF_MARKET_HEADERS = {"platform": 'pc'}

    WF_API = "https://api.warframestat.us"

    TIMER = 600

    bot_category = "warframe-info"
    trade_channel = "trade-info"
    world_state_channel = "world-state-info"


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
