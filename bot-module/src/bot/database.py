import redis
from bot.settings import Settings
from logger import log

__redis_client = redis.Redis(Settings.REDIS_HOST, Settings.REDIS_PORT)
print(__redis_client)


@log(f"{__name__}", 'get keys from pattern')
def get_keys_gen(pattern) -> str:
    for key in __redis_client.keys(f"{pattern}*"):
        key: bytes
        yield key.decode().capitalize()
