from grabber.settings import Settings
from logger import log

settings = Settings()


# r = get(settings.url, headers=settings.headers)
# print(r.status_code)
# data = r.json()
# print(r.text)


@log("prefix", 'msg', param1='val1')
def start():
    print('ffff')


start()
