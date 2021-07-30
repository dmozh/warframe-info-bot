from discord import Embed

from ..settings import settings
from .base import BaseService, Services

from discord.ext.commands import Context
from discord.message import Message

from itertools import chain
from json import loads
from requests import get, Response
from enum import Enum


def request(platform: str, command: str, language: str) -> Response:
    if '_' in command:
        print(command)
        endpoint = command \
                       .replace(
            f'_{command[command.find("_") + 1]}',
            f'{command[command.find("_") + 1].upper()}')[1:].split(' ')[0]
    else:
        endpoint = command[1::].split(' ')[0]
    print(settings.WF_API + f"/{platform}/{endpoint}?language={language}")
    return get(settings.WF_API + f"/{platform}/{endpoint}?language={language}")


class WorldStateService(BaseService):
    def __init__(self, author, collection: Services, ctx: Context):
        super().__init__(author, collection)

        self._ctx = ctx
        self.msg = None

        self.__category = None
        self.__channel = None

    async def cancel(self):
        """
        This function canceled to create new service in collections
        :return:
        """
        await super(WorldStateService, self).cancel()
        await self.author.send("The limit of active a search queries has been exceeded")

    async def remove(self):
        """
        Remove service from collection
        :return:
        """
        await super(WorldStateService, self).remove()

    async def action_on_command(self, command, platform, language):
        if self.__category is None:
            if settings.bot_category in [category.name for category in self._ctx.guild.categories]:
                self.__category = list((category for category in self._ctx.guild.categories if
                                        category.name == settings.bot_category))[0]
            else:
                self.__category = await self._ctx.guild.create_category(settings.bot_category)

        if self.__category:
            if self.__channel is None:
                if settings.world_state_channel in [channel.name for channel in self.__category.text_channels]:
                    self.__channel = list((channel for channel in self.__category.text_channels if
                                           channel.name == settings.world_state_channel))[0]
                else:
                    self.__channel = await self.__category.create_text_channel(settings.world_state_channel)
            if self.__channel:
                if self.msg:
                    pass
                else:
                    response = request(platform, command, language)

                    self.msg = await self.__channel.send(f"{str(response.text)}")
                    await self.remove()
        else:
            await self._ctx.send(f"Категория {settings.bot_category} не создана")
