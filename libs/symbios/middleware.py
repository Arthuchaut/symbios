'''
@desc    The Symbios middleware manager class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import List, Callable, Awaitable, Any
from copy import copy

from . import DeliveredMessage
from .message import IncomingMessage


class Middleware:
    '''Create a middleware from an awaitable.

    Attributes:
        task (Callable[[Symbios, IncMessage], Awaitable[Any]]): The task to
            stack in the middleware queue.
    '''

    def __init__(
        self,
        task: Callable[[object, IncomingMessage], Awaitable[Any]],
        *,
        ephemeral: bool = False
    ):
        '''The Middleware initializer.

        Args:
            task (Callable[[Symbios, IncomingMessage], Awaitable[Any]]): 
                The task to stack in the middleware queue.
        '''

        self.task: Callable[[object, IncomingMessage], Awaitable[Any]] = task
        self.ephemeral: bool = ephemeral


class MiddlewareQueue:
    '''The middleware queue manager.

    Manage middlewares and run all tasks when a consume event are triggered.

    Attributes:
        _stack (List[Middleware]): The Middleware queue.
    '''

    def __init__(self):
        '''The MiddlewareQueue initializer.
        '''

        self._stack: List[Middleware] = []

    def append(self, midd: Middleware) -> None:
        '''Stack the middleware in the queue.

        Args:
            midd (Middleware): The middleware to stack.
        '''

        self._stack.append(midd)

    async def run_until_end(
        self, symbios: object, message: IncomingMessage
    ) -> Awaitable[Any]:
        '''Run all middlewares in queue.

        This method have to be called by the aiormq consumer.

        Args:
            message (DeliveredMessage): The aiormq delivered message.
        '''

        # A temporary solution before implement a much optimized mechanisme.
        tmp_queue: List[Middleware] = copy(self._stack)

        for midd in tmp_queue:
            await midd.task(symbios, message)

            if midd.ephemeral:
                self._stack.remove(midd)
