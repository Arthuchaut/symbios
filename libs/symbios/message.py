'''
@desc    The message class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import Any
from abc import ABC


class Message(ABC):
    def __init__(self, body: bytes):
        ...

    def serialize(self) -> str:
        ...

    def deserialize(self) -> Any:
        ...


class IncMessage(Message):
    ...


class SenMessage(Message):
    ...
