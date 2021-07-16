from ..database import get_keys_gen
from discord.ext.commands import Context
from discord.message import Message
from math import ceil
from itertools import chain

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


class TradeService:
    __all_items = []
    __pages = 1
    __page = 0

    def __init__(self, ctx):
        self.ctx = ctx

    def __get_items(self, items: tuple):
        """
        :param items:
        :return:
        """
        print(items)
        if not self.__all_items:
            keys = [str(item).lower() for item in items]
            self.__all_items.extend(chain(*[get_keys_gen(pattern=f'{key}') for key in keys]))
        self.__pages = ceil(len(self.__all_items) / SHOWED_ITEMS)

    def gen_msg(self, items: tuple = None) -> str:
        if items:
            self.__get_items(items)

        msg = f"{self.ctx.message.author.mention}```Вы ищите: \n"
        it = 1
        for index in range(1 + (self.__page*10), len(self.__all_items)):
            _tmp = msg
            if len(msg) < 2000 and it <= SHOWED_ITEMS:
                msg += f"{index}. {self.__all_items[index]}\n"
                it += 1
                if len(msg) >= 2000:
                    msg = _tmp
                    break
        else:
            if len(self.__all_items) > 10:
                msg += f"И еще {len(self.__all_items) - it} возможных предмета"
            msg += "```"

        return msg

    def select_page(self, reaction, user):
        if user == self.ctx.message.author:
            if str(reaction) == emoji["previous"]:
                self.__page -= 1
            elif str(reaction) == emoji["next"]:
                self.__page += 1
            else:
                pass
            return self.gen_msg()

    @staticmethod
    async def add_reactions(msg: Message):
        i = 1
        while i <= SHOWED_ITEMS:
            await msg.add_reaction(emoji[i])
            i += 1
        await msg.add_reaction(emoji["previous"])
        await msg.add_reaction(emoji["next"])

    def return_ctx(self) -> Context:
        return self.ctx

    def __del__(self):
        """"""
