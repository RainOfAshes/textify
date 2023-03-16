import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Callable, List, Union

from joblib import Parallel, delayed


class Pipeline:
    def __init__(self, *callables: Callable):
        self.__callables = list(callables)

    def _apply(self, text: str) -> str:
        for callable_ in self.__callables:
            text = callable_(text)
        return text

    def __call__(self, text: Union[str, List[str]], n_jobs: int = -2) -> Union[str, List[str]]:
        if isinstance(text, str):
            return self._apply(text)
        elif isinstance(text, list):
            return Parallel(n_jobs=n_jobs)(delayed(self.__call__)(t) for t in text)
        else:
            raise TypeError("Input text must be a string or a list of strings")


standard_prefix = "%Y-%m-%d"


def get_logger(logs_dir, logger_name):
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    info_handler = TimedRotatingFileHandler(
        os.path.join(logs_dir, "info.log"),
        when="midnight", interval=1, utc=True, encoding='utf-8')

    info_handler.setLevel(logging.INFO)
    info_handler.suffix = standard_prefix

    error_handler = TimedRotatingFileHandler(
        os.path.join(logs_dir, "errors.log"),
        when="midnight", interval=1, utc=True, encoding='utf-8')

    error_handler.setLevel(logging.ERROR)
    error_handler.suffix = standard_prefix
    message_format = '%(asctime)s UTC %(levelname)s %(message)s'
    formatter = logging.Formatter(message_format, datefmt="%d-%m-%Y %H:%M:%S")

    info_handler.setFormatter(formatter), error_handler.setFormatter(formatter)

    logger.addHandler(info_handler), logger.addHandler(error_handler)

    return logger
