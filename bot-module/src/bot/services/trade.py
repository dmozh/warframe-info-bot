from ..database import get_keys_gen, get_item
from ..settings import settings
from .base import BaseService, Services

from discord.ext.commands import Context
from discord.message import Message
from discord import Embed

from itertools import chain
from json import loads
from requests import get
from enum import Enum



SHOWED_ITEMS = 10

emoji = {1: "1️⃣",
         2: "2️⃣",
         3: "3️⃣",
         4: "4️⃣",
         5: "5️⃣",
         6: "6️⃣",
         7: "7️⃣",
         8: "8️⃣",
         9: "9️⃣",
         10: "🔟",
         "next": "➡",
         "previous": "⬅"}


class MessageState(Enum):
    pass


class TradeService(BaseService):

    def __init__(self, author, collection: Services, ctx: Context):
        """
        Constructor
        :param author: key for limiting to create services
        :param collection: Collection where will be saving created service
        :param ctx: Context object from discord.py module
        """
        super().__init__(author, collection)
        self._ctx = ctx
        self.msg = None  # Last msg object
        self.msg_state = None  # Currently no used
        # Msg state for the difference which msg currently used

        self.__all_items = []
        self.__pages = 1
        self.__page = 0
        self.__item: dict = {}

        self.__category = None
        self.__channel = None

    async def cancel(self):
        """
        This function canceled to create new service in collections
        :return:
        """
        await super(TradeService, self).cancel()
        await self.author.send("The limit of active a search queries has been exceeded")

    async def remove(self):
        """
        Remove service from collection
        :return:
        """
        await super(TradeService, self).remove()
        await self.clear_reactions()
        await self.edit_msg(content=f"Законченный поиск\n{self.msg.content}", embed=self.msg.embeds[0])

    def __get_items(self, needed_items: tuple):
        """
        Get needed_items from redis db
        :param needed_items: tuple, needed trade items which find user
        :return:
        """
        # keys =
        self.__all_items \
            .extend(chain(*[get_keys_gen(pattern=f'{key}') for key in [str(item).lower() for item in needed_items]]))
        self.__pages = round(len(self.__all_items) / SHOWED_ITEMS)

    async def action_on_msg(self, **kwargs):
        """
        Execute when bot get msg
        :param kwargs:
        :return:
        """
        if self.__category is None:
            if settings.bot_category in [category.name for category in self._ctx.guild.categories]:
                self.__category = list((category for category in self._ctx.guild.categories if
                                        category.name == settings.bot_category))[0]
            else:
                self.__category = await self._ctx.guild.create_category(settings.bot_category)
        # print(self.__category.text_channels)
        if self.__category:
            if self.__channel is None:
                if settings.trade_channel in [channel.name for channel in self.__category.text_channels]:
                    self.__channel = list((channel for channel in self.__category.text_channels if
                                           channel.name == settings.trade_channel))[0]
                else:
                    self.__channel = await self.__category.create_text_channel(settings.trade_channel)
            if self.__channel:
                if self.msg:
                    pass
                else:
                    text = self._gen_general_msg(kwargs['items'])
                    self.msg = await self.__channel.send(f"{text}")
                    await self.add_reactions(self.msg)
        else:
            await self._ctx.send(f"Категория {settings.bot_category} не создана")

    async def action_on_reaction(self, reaction, user):
        """
        Execute when user set reaction on msg from bot
        :param reaction:
        :param user:
        :return:
        """
        if user == self._ctx.message.author and self.msg.id == reaction.message.id:
            if str(reaction) != emoji["previous"] and str(reaction) != emoji["next"]:
                for key, value in emoji.items():
                    if str(reaction) == value:
                        content, embed = self._gen_trade_item_msg(key)
                        await self.edit_msg(content=content, embed=embed)
                        await self.remove()
            else:
                if str(reaction) == emoji["previous"]:
                    if self.__page != 0:
                        self.__page -= 1
                    else:
                        self.__page = self.__pages
                elif str(reaction) == emoji["next"]:
                    if self.__page != self.__pages:
                        self.__page += 1
                    else:
                        self.__page = 0
                else:
                    pass
                await self.edit_msg(msg=reaction.message, content=self._gen_general_msg())
                await self.add_reactions(reaction.message)

    def _gen_general_msg(self, items: tuple = None):
        if items:
            self.__get_items(items)
        if len(self.__all_items) > 0:
            text = f"{self._ctx.message.author.mention}, ваш запрос на поиск следующих предметов: {str(*items)}" \
                   f"```Возможно вы ищите: \n"
            it = 1
            for index in range(0 + (self.__page * 10), len(self.__all_items)):
                _tmp = text
                if len(text) < 2000 and it <= SHOWED_ITEMS:
                    text += f"{index + 1}. {self.__all_items[index]}\n"
                    it += 1
                    if len(text) >= 2000:
                        text = _tmp
                        break
            if len(self.__all_items) > 10:
                text += f"И еще {len(self.__all_items) - it} возможных предмета"
            text += "```"
        else:
            text = "```" \
                   "Упс.. Ничего не найдено, попробуйте еще раз" \
                   "```"
        return text
        # self.msg = await self._ctx.send(f"{text}")
        # await self.add_reactions(self.msg)

    def _gen_trade_item_msg(self, key: int):
        # print(key, self.__page)
        self.__item = loads(get_item(self.__all_items[key + (self.__page * 10) - 1].lower()).decode(encoding='utf8'))
        # print(self.__item)
        response = get(settings.WF_MARKET_API_HOST + f"/items/{self.__item['url_name']}/orders",
                       headers=settings.WF_MARKET_HEADERS)
        orders = sorted(response.json()['payload']["orders"], key=lambda item: item['platinum'])
        text = f"{self._ctx.message.author.mention}```\n"
        it = 1
        for order in orders:
            _tmp = text
            if len(text) < 2000 and it <= SHOWED_ITEMS:
                if order['order_type'] == 'sell' and order['user']['status'] == 'ingame':
                    text += f"{it}. Игрок {order['user']['ingame_name']} продает {order['quantity']} шт. по цене за шт. {order['platinum']}\n"
                    it += 1
            else:
                text = _tmp
                break
        text += "```"
        embed = Embed(color=0xff9900, title=f'{self.__item["item_name"].capitalize()}')
        try:
            embed.set_image(url=self.__item['thumb'])
        except Exception as e:
            pass
        # self.msg = await self._ctx.send(text, embed=embed)
        return text, embed

    async def add_reactions(self, msg: Message):
        i = 1
        _limit = \
            len(self.__all_items) if len(self.__all_items) < SHOWED_ITEMS \
                else len(self.__all_items) - self.__pages * SHOWED_ITEMS \
                if self.__page == self.__pages else SHOWED_ITEMS

        while i <= _limit:
            await msg.add_reaction(emoji[i])
            i += 1
        else:
            if len(self.__all_items) > 0:
                await msg.add_reaction(emoji["previous"])
                await msg.add_reaction(emoji["next"])

    async def edit_msg(self, msg: Message = None, content: str = None, embed: Embed = None):
        if msg:
            await msg.clear_reactions()
            await msg.edit(content=content, embed=embed)
        else:
            await self.msg.clear_reactions()
            await self.msg.edit(content=content, embed=embed)

    async def clear_reactions(self):
        await self.msg.clear_reactions()

    async def delete_last_msg(self):
        await self.msg.delete()
        self.msg = None
        self.msg_state = None

    @property
    def ctx(self) -> Context:
        return self._ctx


# services = Services()