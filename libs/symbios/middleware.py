'''
@desc    The Symbios middleware manager class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import List, Awaitable

from . import Symbios


class Middleware:
    def __init__(self, self_symbios: Symbios):
        ...

