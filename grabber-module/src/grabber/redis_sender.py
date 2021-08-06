import redis
from grabber.settings import settings
from json import dumps
from logger import log

__redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def set_value(item: dict):
    _data = dumps(item)
    __redis_client.set(item['item_name'], _data)