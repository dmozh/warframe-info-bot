class Settings:
    # default
    url = "https://api.warframe.market/v1/items"
    static_url = "https://warframe.market/static/assets/"
    headers = {"Language": "ru"}

    def __init__(self):
        pass

    def set_settings(self,
                     url: str=None,
                     static_url: str=None,
                     headers: dict=None):
        if url:
            self.url = url
        if static_url:
            self.static_url = static_url
        if headers:
            for key, value in headers.items():
                self.headers[key] = value