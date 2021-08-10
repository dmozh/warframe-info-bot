import redis
from settings import settings
from json import dumps
from logger import log

__redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


@log(f"grabber.redis_sender", "set value in redis")
def set_value(item: dict):
    _data = dumps(item)
    __redis_client.set(item['item_name'], _data)
