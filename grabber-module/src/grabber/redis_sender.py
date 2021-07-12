import redis
from grabber.settings import Settings
import json
from datetime import datetime

from time import sleep

# __redis_client = redis.Redis(host=Settings.REDIS_HOST, port=Settings.REDIS_PORT)


def set_value(item: dict):
    for key, value in item.items():
        print(key, value)
    sleep(10)