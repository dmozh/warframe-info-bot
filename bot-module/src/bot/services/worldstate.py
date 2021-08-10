from discord import Embed

from settings import settings
from .base import BaseService, Services

from discord.ext.commands import Context
from discord.message import Message

from requests import get, Response
from datetime import datetime, timedelta
from enum import Enum


class KeyStorm(str, Enum):
    ALL = "all"
    PLANET = "planet"
    STORM = "storm"


# unusage
class EnemyKey(str, Enum):
    ALL = "all"
    GRINEER = "grineer"
    CORPUS = "corpus"


class KeyTier(str, Enum):
    ALL = "0"
    LIT = "1"
    MEZO = "2"
    NEO = "3"
    AXI = "4"
    REQUIEM = "5"


def request(command: str, platform: str, language: str) -> Response:
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

    async def action_on_command(self, command, platform, language, **kwargs):
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
                    response = request(command, platform, language)
                    if response.status_code == 404:
                        text = f"{self._ctx.message.author.mention}\n" \
                               f"Ничего не найдено по запросу command={command.split(' ')[0]} platform={platform} language={language}"
                    else:
                        if str(response.text) != '[]':
                            if "$void_trader" in command:
                                text = self.generate_msg_void_trader(response)
                            elif ("$earth_cycle" in command) or ("$cetus_cycle" in command) or (
                                    "$cambion_cycle" in command):
                                text = self.generate_msg_location(response)
                            elif "$invasions" in command:
                                text = self.generate_msg_invasions(response)
                            elif "$alerts" in command:
                                text = self.generate_msg_alerts(response)
                            elif "$fissures" in command:
                                text = self.generate_msg_fissures(response, kwargs['key_storm'], kwargs["key_tier"])
                            elif "$sortie" in command:
                                text = self.generate_msg_sortie(response)
                            elif "$events" in command:
                                text = self.generate_msg_events(response)
                            else:
                                text = f"{self._ctx.message.author.mention}\nНеизвестная команда"
                        else:
                            text = f'{self._ctx.message.author.mention}\nНикаких данных на данный момент нет'
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
            text = f'{self._ctx.message.author.mention}\n{_data["character"]} прибыл на локацию {_data["location"]}, уедет через {_data["endString"].replace("d", " дней").replace("h", f" часов").replace("m", _)[0:-3]}\n' \
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

            return f'{self._ctx.message.author.mention}\nНа текущий момент {_data["character"]} не прибывает ни на одном реле\n' \
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
        return f"{self._ctx.message.author.mention}\nТекущая фаза {state}"

    def generate_msg_invasions(self, response: Response):
        _data = list(filter(lambda x: x['completed'] is False, response.json()))
        print(len(_data))
        if len(_data) == 1:
            skl = "вторжение"
        elif len(_data) == 2:
            skl = "вторжения"
        elif len(_data) > 20:
            if len(_data) % 10 == 1:
                skl = "вторжение"
            elif len(_data) % 10 == 2:
                skl = "вторжения"
        else:
            skl = "вторжений"
        text = f"{self._ctx.message.author.mention}\n" \
               f"Доступно {len(_data)} {skl}:\n"

        for item in _data:
            a_reward = f"предлагает {item['attackerReward']['itemString']}" \
                if item['attackerReward']['itemString'] != "" \
                else "ничего не предлагает"
            d_reward = f"предлагает {item['defenderReward']['itemString']}" \
                if item['defenderReward']['itemString'] != "" \
                else "ничего не предлагает"
            text += f"{item['desc']} на {item['node']}\n" \
                    f"Детали:\n" \
                    f"```" \
                    f"  --> Атакующая фракция {item['attackingFaction']} " \
                    f"{a_reward}\n" \
                    f"  --> Обороняющаяся фракция {item['defendingFaction']} " \
                    f"{d_reward}\n" \
                    f"  --> Вторжение будет длиться еще {item['eta']}" \
                    f"```\n"
        return text

    def generate_msg_alerts(self, response: Response):
        _data = response.json()
        print(_data)
        return str(_data)

    def generate_msg_fissures(self, response: Response, storm: KeyStorm, tier: KeyTier):
        _data = list(filter(lambda x: x['active'] is True, response.json()))
        if storm == KeyStorm.STORM:
            _data = list(filter(lambda x: x['isStorm'] is True, _data))
        elif storm == KeyStorm.PLANET:
            _data = list(filter(lambda x: x['isStorm'] is False, _data))
        else:
            pass
        if tier != KeyTier.ALL:
            _data = list(filter(lambda x: x['tierNum'] == int(tier.value), _data))
        _data = list(sorted(_data, key=lambda x: x['tierNum']))

        text = f"{self._ctx.message.author.mention}\n" \
               f"Текущие разрывы бездны\n"
        _lit_block = "Уровень Лит:" \
                     "\n```"
        _mezo_block = "Уровень Мезо:" \
                      "\n```"
        _neo_block = "Уровень Нео:" \
                     "\n```"
        _axi_block = "Уровень Акси:" \
                     "\n```"
        _requiem_block = "Уровень Реквием:" \
                         "\n```"
        for item in _data:
            if item['tierNum'] == 1:
                _lit_block += f"--> На узле {item['node']} миссия типа {item['missionType']} с '{item['enemy']}' " \
                              f"будет активна еще {item['eta']}\n"
            elif item['tierNum'] == 2:
                _mezo_block += f"--> На узле {item['node']} миссия типа {item['missionType']} с '{item['enemy']}' " \
                               f"будет активна еще {item['eta']}\n"
            elif item['tierNum'] == 3:
                _neo_block += f"--> На узле {item['node']} миссия типа {item['missionType']} с '{item['enemy']}' " \
                              f"будет активна еще {item['eta']}\n"
            elif item['tierNum'] == 4:
                _axi_block += f"--> На узле {item['node']} миссия типа {item['missionType']} с '{item['enemy']}' " \
                              f"будет активна еще {item['eta']}\n"
            elif item['tierNum'] == 5:
                _requiem_block += f"--> На узле {item['node']} миссия типа {item['missionType']} с '{item['enemy']}' " \
                                  f"будет активна еще {item['eta']}\n"
            else:
                pass
        else:
            _lit_block += "```"
            _mezo_block += "```"
            _neo_block += "```"
            _axi_block += "```"
            _requiem_block += "```"
        if tier == KeyTier.ALL:
            text += _lit_block + "\n" + _mezo_block + "\n" + _neo_block + "\n" + _axi_block + "\n" + _requiem_block
        else:
            if tier == KeyTier.LIT:
                text += _lit_block
            elif tier == KeyTier.MEZO:
                text += _mezo_block
            elif tier == KeyTier.NEO:
                text += _neo_block
            elif tier == KeyTier.AXI:
                text += _axi_block
            else:
                text += _requiem_block
        print(len(text))
        return text

    def generate_msg_sortie(self, response: Response):
        _data = response.json()
        activation = datetime.strptime(_data['activation'], '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=3)
        text = f"{self._ctx.message.author.mention}\n" \
               f"Информация о текущей вылазке: \n" \
               f"  --> запущена {activation.date()} в {activation.time()} по Москве (+3)\n" \
               f"  --> фракция {_data['faction']}\n" \
               f"  --> босс {_data['boss']}\n" \
               f"  --> миссии: \n"
        for v in _data['variants']:
            text += f'На узле {v["node"]}\n'
            text += f'```' \
                    f'Тип миссии: {v["missionType"]}\n' \
                    f'Модификатор: {v["modifier"]}\n' \
                    f'Описание модификатора: {v["modifierDescription"]}\n' \
                    f'```\n'
        activation += timedelta(days=1)
        text += f"Новая вылазка начнется {activation.date()} в {activation.time()} по Москве (+3)"
        print(_data)
        return str(text)

    def generate_msg_events(self, response: Response):
        _data = response.json()
        print(_data)
        return str(_data)
