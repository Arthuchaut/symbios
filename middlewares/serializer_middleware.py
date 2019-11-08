'''
@desc    The serializer middleware for Symbios.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-22
@note    0.1.0 (2019-09-22): Writed the first drafts.
'''

from typing import Union, Dict, Any
import json

from symbios.middleware import MiddlewareABC
from symbios.message import SendingMessage


class SerializerMiddleware(MiddlewareABC):
    '''The SerializerMiddleware class declaration.

    Attributes:
        _type_corr (Dict[str, Any]): The typing converter dictionnary.
    '''

    def __init__(self, event: int):
        '''The SerializerMiddleware initializer.

        Args:
            event (int): The event associated with middleware.
        '''

        super().__init__(event)

        self._type_corr: Dict[str, Any] = {
            str: self._str_to_bytes,
            int: self._str_to_bytes,
            float: self._str_to_bytes,
            dict: self._dict_to_bytes,
        }

    async def execute(self, symbios: object, message: SendingMessage) -> None:
        '''Serialize the message.

        Implement the serialized attribute to the message.

        Args:
            symbios (Symbios): The symbios instance.
            message (SendingMessage): The message to send. 

        Raises:
            SerializerMiddlewareError: If the type of message is 
                not serializable.
        '''

        try:
            setattr(
                message,
                'serialized',
                self._type_corr[type(message.body)](message.body),
            )
        except KeyError as e:
            raise SerializerMiddlewareError(
                f'Type {type(message.body).__name__} is not serializable.'
            )

    def _str_to_bytes(self, body: Union[str, int, float]) -> bytes:
        '''Parse the body string to bytes.

        Args:
            body (Union[str, int, float]): The message body to parse.

        Returns:
            bytes: The body parsed.
        '''

        return str(body).encode()

    def _dict_to_bytes(self, body: Dict[Any, Any]) -> bytes:
        '''Parse the Dict[Any, Any] body to a stringify JSON bytes.

        Args:
            body (Dict[Any, Any]): The message body to parse.

        Returns:
            bytes: The body parsed.
        '''

        return json.dumps(body).encode()


class SerializerMiddlewareError(Exception):
    '''The SerializerMiddlewareError Exception class.
    '''

    def __init__(self, message: str):
        super().__init__(message)
