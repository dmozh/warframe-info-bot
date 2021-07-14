from .services import general, trade


class Dialog:
    __author = None
    __service = None

    def __int__(self, author: str, service: object):
        self.__author = author
        self.__service = service
