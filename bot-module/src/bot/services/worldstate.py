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
                    if str(response.text) != '[]':
                        if "$void_trader" in command:
                            text = self.generate_msg_void_trader(response)
                        elif "$earth_cycle" or "$cetus_cycle" or "$cambion_cycle" in command:
                            text = self.generate_msg_location(response)
                        else:
                            text = f"Неизвестная команда"
                    else:
                        text = 'Никаких данных на данный момент нет'

                    self.msg = await self.__channel.send(f"{text}")
                    await self.remove()
        else:
            await self._ctx.send(f"Категория {settings.bot_category} не создана")

    def generate_msg_void_trader(self, response: Response):
        _data = response.json()
        if _data['active']:
            _ = _data['endString'][_data['endString'].rfind('m') - 1]
            if int(_) == 1:
                _ = " минуту"
            elif int(_) == 2:
                _ = " минуты"
            else:
                _ = " минут"
            text = f'{_data["character"]} прибыл на локацию {_data["location"]}, уедет через {_data["endString"].replace("d", " дней").replace("h", f" часов").replace("m", _)[0:-3]}\n' \
                   f'Предложения: \n'
            items = f'```\n'
            for item in _data["inventory"]:
                items += f'{item["item"]} по цене в {item["ducats"]} дукатов и {item["credits"]} кредитов\n'
            else:
                text += f'{items}```'
            return text
        else:
            _ = _data['startString'][_data['startString'].rfind('m') - 1]
            if int(_) == 1:
                _ = " минуту"
            elif int(_) == 2:
                _ = " минуты"
            else:
                _ = " минут"

            return f'На текущий момент {_data["character"]} не прибывает ни на одном реле\n' \
                   f'Ожидайте {_data["character"]} через {_data["startString"].replace("d", " дней").replace("h", f" часов").replace("m", _)[0:-3]} ' \
                   f'на локации {_data["location"]}'

    def generate_msg_location(self, response: Response):
        _data = response.json()
        if "cambion" in _data['id']:
            if _data['active'] == "fass":
                state = "Фэз"
            else:
                state = "Воум"
        elif "cetus" in _data['id']:
            if _data['isDay']:
                state = "Тепло"
            else:
                state = "Холод"
        elif "earth" in _data['id']:
            if _data['isDay']:
                state = "День"
            else:
                state = "Ночь"
        else:
            return "Нет данных"
        return f"Текущая фаза {state}"
