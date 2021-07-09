from functools import wraps

import logging.config
import os

if os.path.exists("../../logs"):
    pass
else:
    os.mkdir("../../logs")
logging.config.fileConfig(os.path.abspath('../logger.conf'))

info_logger, traceback_logger = logging.getLogger("infoLogger"), logging.getLogger("errorLogger")


def log(prefix_msg: str, msg: str, log_coro: bool = False, **params):
    """
    Создание лога
    :param log_coro: bool flag for coroutine log
    :param prefix_msg: str
    :param msg: str
    :param params: dict
    """

    def generate_log(func):
        """
        Внутренний декоратор для генерации сообщения для лога
        :param func: obj executable function
        :return:
        """
        log = f"| function {func} | {prefix_msg}: {msg}\n"
        if params:
            log += f"Additional info:"
            for key, value in params.items():
                log += f"\n{key}: {value}"

        if log_coro:
            @wraps(func)
            async def _logging(*args, **kwargs):
                try:
                    await func(*args, **kwargs)
                    info_logger.info(log)
                except Exception as e:
                    _log = f"{log}\n {e}"
                    traceback_logger.error(_log)
        else:
            def _logging(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                    info_logger.info(log)
                except Exception as e:
                    _log = f"{log}\n {e}"
                    traceback_logger.error(_log)
        return _logging

    return generate_log
