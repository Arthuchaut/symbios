'''
@desc    The body deserializer middleware for Symbios.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-22
@note    0.1.0 (2019-09-22): Writed the first drafts.
'''

from typing import Union, Dict, Any
import json

from symbios.middleware import MiddlewareABC
from symbios.message import IncomingMessage


class DeserializerMiddleware(MiddlewareABC):
    '''The DeserializerMiddleware class declaration.

    Attributes:
        _content_type_corr (Dict[str, Any]): The content-type
            correlation dictionnary.
    '''

    def __init__(self, event: int):
        '''The DeserializerMiddleware initializer.

        Args:
            event (int): The event associated with middleware.
        '''

        super().__init__(event)

        self._content_type_corr: Dict[str, Any] = {
            'text/plain': self._bytes_to_str,
            'application/json': self._bytes_to_dict,
        }

    async def execute(self, symbios: object, message: IncomingMessage) -> None:
        '''Implement to the message the deserialized format.
        '''

        content: Union[str, Dict[str, Any]] = None

        try:
            content = self._content_type_corr[message.props.content_type](
                message.body
            )
        except KeyError as e:
            content = self._bytes_to_str(message.body)

        setattr(message, 'deserialized', content)

    def _bytes_to_str(self, body: bytes) -> str:
        '''Parse the body to string.

        Args:
            body (bytes): The message body to parse.

        Returns:
            str: The body parsed.
        '''

        return body.decode()

    def _bytes_to_dict(self, body: bytes) -> Dict[str, Any]:
        '''Parse the body to Dict[str, Any].

        Args:
            body (bytes): The message body to parse.

        Returns:
            Dict[str, Any]: The body parsed.
        '''

        return json.loads(self._bytes_to_str(body))
