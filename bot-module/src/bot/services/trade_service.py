from ..database import get_keys_gen


class TradeService:
    __items = []
    __pages = 0

    def __init__(self):
        pass

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

        msg = "```Вы ищите: \n"
        for item in self.__items:
            _tmp = msg
            if len(msg) < 2000:
                msg += f"-{item}\n"
                if len(msg) >= 2000:
                    msg = _tmp
                    break
        else:
            msg += "```"
        return msg
