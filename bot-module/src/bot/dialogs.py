from .services import general, trade

DIALOGS = {}


class Dialog:
    __author = None
    __service = None

    def __init__(self, author: str, service: object):
        self.__author = author
        self.__service = service

    def answer(self, func):
        return func
