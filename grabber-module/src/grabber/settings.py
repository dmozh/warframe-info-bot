class Settings:
    # default
    url = "https://api.warframe.market/v1/items"
    static_url = "https://warframe.market/static/assets/"
    headers = {"Language": "ru"}

    REDIS_HOST = ''
    REDIS_PORT = ''

    def __init__(self):
        pass

    def set_settings(self,
                     url: str = None,
                     static_url: str = None,
                     headers: dict = None,
                     redis_port: str = None,
                     redis_host: str = None):
        if url:
            self.url = url
        if static_url:
            self.static_url = static_url
        if headers:
            for key, value in headers.items():
                self.headers[key] = value
        if redis_port:
            self.REDIS_PORT = redis_port
        if redis_host:
            self.REDIS_HOST = redis_host
