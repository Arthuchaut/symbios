'''
@desc    The Symbios middleware manager classes.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-22
@note    0.1.0 (2019-09-22): Writed the first drafts.
'''

from typing import Union, List
from enum import Enum
from abc import ABC, abstractmethod

from .message import IncomingMessage, SendingMessage


class Event(Enum):
    '''The Event enumeration declaration.

    Allows to define the ownership of the event of a middleware.

    Attributes:
        ON_EMIT (int): Refer to the emitter.
        ON_LISTEN (int): Refer to the listener.
    '''

    ON_EMIT: int = 0
    ON_LISTEN: int = 1


class MiddlewareABC(ABC):
    '''The MiddlewareABC declaration.

    Abstract class for defining middleware.

    Attributes:
        event (int): The event associated with middleware.
    '''

    def __init__(self, event: int):
        '''The MiddlewareABC initializer.

        Args:
            event (int): The event associated with middleware.
        '''

        self.event: int = event

    @abstractmethod
    async def execute(
        self, symbios: object, message: Union[IncomingMessage, SendingMessage]
    ) -> None:
        '''Abstract method that contains the middleware processes.

        Args:
            symbios (Symbios): The Symbios instance.
            message (Union[IncomingMessage, SendingMessage]): 
                The received or sending message.
        '''

        pass


class MiddlewareLibrary:
    '''The MiddlewareLibrary class declaration.

    Allows to register the defined middlewares.

    Attributes:
        _library (Dict[int, List[MiddlewareABC]]): The library that 
            contains all declared middlewares.
    '''

    def __init__(self):
        '''The MiddlewareLibrary initializer.
        '''

        self._library: Dict[int, List[MiddlewareABC]] = {
            Event.ON_EMIT: [],
            Event.ON_LISTEN: [],
        }

    def append(self, midd: MiddlewareABC) -> None:
        '''Register a middleware to the library.

        Args:
            midd (MiddlewareABC): The middleware instance to register.

        Raises:
            MiddlewareLibraryError: If the midd argument is not a subclass
                of MiddlewareABC.
        '''

        if not isinstance(midd, MiddlewareABC):
            raise MiddlewareLibraryError(
                f'Expected an instance of MiddlewareABC, {type(midd)} given.'
            )

        self._library[midd.event].append(midd)

    async def run_until_end(
        self, symbios: object, message: SendingMessage, event: int
    ) -> None:
        '''Call all defined middlewares associated the event specified.

        Args:
            symbios (Symbios): The Symbios instance.
            message (Union[IncomingMessage, SendingMessage]): The 
                listener/emiter message.
        '''

        for midd in self._library[event]:
            await midd.execute(symbios, message)


class MiddlewareLibraryError(Exception):
    '''The MiddlewareLibraryError exception class.
    '''

    def __init__(self, message: str):
        '''The MiddlewareLibraryError initializer.

        Args:
            message (str): The message to raise.
        '''

        super().__init__(message)
