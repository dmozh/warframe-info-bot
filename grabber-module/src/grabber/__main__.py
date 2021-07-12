from grabber.settings import Settings
from grabber.redis_sender import set_value
from logger import log
from time import sleep
from requests import get

settings = Settings()
WORK = True
WAIT = 86400


# r = get(settings.url, headers=settings.headers)
# print(r.status_code)
# data = r.json()
# print(r.text)
@log(f"grabber.{__name__}", "grab data for trading items")
def grab():
    data = {}
    try:
        r = get(settings.url, headers=settings.headers)
        data = r.json()
        # print(r.text)
    except Exception:
        exit(1)

    for item in data['payload']['items']:
        item['item_name'] = item['item_name'].lower()
        item['thumb'] = settings.static_url+item['thumb']
        set_value(item)


@log(f"grabber.{__name__}", 'start program')
def start():
    while WORK:
        grab()
        sleep(WAIT)


if __name__ == '__main__':
    start()
