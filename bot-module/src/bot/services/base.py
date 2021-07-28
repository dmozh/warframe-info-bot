from ..settings import settings

import asyncio


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()


class Services:
    __limits = 5

    def __init__(self):
        """
        Constructor
        """
        self.services = []
        self.authors = {}

    async def add_service(self, author, service):
        """
        add service to collection for manage him
        :param author: Member object from discord.py module
        :param service: TradeService object
        :return:
        """
        added = False
        if author not in self.authors:
            self.authors[author] = 0
        if self.authors[author] < self.__limits:
            self.services.append(service)
            self.authors[author] += 1
            added = True
        else:
            await service.cancel()
        return added

    def remove_service(self, author, service):
        self.services.remove(service)
        self.authors[author] -= 1

    def __repr__(self):
        return f"Services <{self.services}>"

    def __len__(self):
        return len(self.services)

    def __getitem__(self, item):
        return self.services[item]


class BaseService:

    def __init__(self, author, collection: Services):
        self.collection = collection
        self.author = author
        self.timer = Timer(settings.TIMER, self.remove)

    async def cancel(self):
        """
        This function canceled to create new service in collections
        :return:
        """
        self.timer.cancel()

    async def remove(self):
        """
        Remove service from collection
        :return:
        """
        self.timer.cancel()
        self.collection.remove_service(self.author, self)


services = Services()
