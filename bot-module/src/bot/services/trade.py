from ..database import get_keys_gen


class TradeService:
    __items = []
    __pages = 0

    def __init__(self, ctx):
        self.ctx = ctx

    def __get_items(self, msg: str):
        """
        :param msg:
        :return:
        """
        keys = msg[msg.find(' ') + 1:].replace(', ', ',').split(',')
        # print(keys)
        # items = []
        for key in keys:
            self.__items.extend(get_keys_gen(pattern=f'{key}'))

    def gen_msg(self, msg: str) -> str:
        self.__get_items(msg)

        msg = f"{self.ctx.message.author.mention}```Вы ищите: \n"
        it = 1
        for item in self.__items:
            _tmp = msg
            if len(msg) < 2000 and it <= 10:
                msg += f"{it}. {item}\n"
                it += 1
                if len(msg) >= 2000 and it > 10:
                    msg = _tmp
                    break
        else:
            if len(self.__items) > 10:
                msg += f"И еще {len(self.__items)-it} возможных предмета"
            msg += "```"
        return msg

    def __del__(self):
        """"""
