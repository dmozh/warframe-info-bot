import redis
from grabber.settings import Settings
from json import dumps
from logger import log

__redis_client = redis.Redis(host=Settings.REDIS_HOST, port=Settings.REDIS_PORT)


def set_value(item: dict):
    _data = dumps(item)
    __redis_client.set(item['item_name'], _data)