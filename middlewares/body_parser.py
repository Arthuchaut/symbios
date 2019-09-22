'''
@desc    The body parser middleware for Symbios.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-22
@note    0.1.0 (2019-09-22): Writed the first drafts.
'''

from libs.symbios.middleware import MiddlewareABC
from libs.symbios.message import IncomingMessage

class BodyParserMiddleware(MiddlewareABC):
    def __init__(self, event: int, priority: int)
        super().__init__(event, priority)

    async def execute(self, symbios: object, message: IncomingMessage) -> None:
        ...