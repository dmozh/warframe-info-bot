import redis
from bot.settings import settings
from logger import log

__redis_client = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT)
print(__redis_client)


@log(f"{__name__}", 'get keys from pattern')
def get_keys_gen(pattern: str) -> str:
    for key in __redis_client.keys(f"{pattern}*"):
        key: bytes
        yield key.decode().capitalize()


@log(f"{__name__}", 'get item')
def get_item(item: str) -> bytes:
    return __redis_client.get(item)
