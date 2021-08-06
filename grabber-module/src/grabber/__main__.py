from grabber.settings import settings
from grabber.redis_sender import set_value
from logger import log
from time import sleep
from requests import get

# settings = Settings()
WORK = True

iteration = 0


@log(f"grabber.{__name__}", "grab data for trading items")
def grab():
    data = {}
    try:
        r = get(settings.url, headers=settings.headers)
        data = r.json()
    except Exception:
        exit(1)

    for item in data['payload']['items']:
        item['item_name'] = item['item_name'].lower()
        item['thumb'] = settings.static_url + item['thumb']
        set_value(item)


@log(f"grabber.{__name__}", f'start program')
def start():
    while WORK:
        grab()
        sleep(settings.WAIT)


if __name__ == '__main__':
    start()
