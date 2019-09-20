'''
@desc    The message class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import Any
from abc import ABC

from . import DeliveredMessage, GetEmpty, GetOk, Props


class IncomingMessage:
    '''The IncomingMessage class declaration.

    This class will be instanciated when a message will incoming from
    the consumer.

    Attributes:
        delivery (Union[GetEmpty, GetOk]): The message ack tag.
        header (Any): The message header.
        props (Props): The message properties.
        body (bytes): The message content.
    '''

    def __init__(self, message: DeliveredMessage):
        '''The IncomingMessage initializer.

        Args:
            message (DeliveredMessage): The aiormq message object.
        '''

        self.delivery: Union[GetEmpty, GetOk] = message.delivery
        self.header: Any = message.header
        self.props: Props = message.header.properties
        self.body: bytes = message.body

    @property
    def deserialized(self) -> Any:
        '''Return the deserialized message body.

        Returns:
            Any: The deserialized message.
        '''

        if self.props.content_type == '':
            return self.body.decode()

        # TODO: Do the type convertion.
        return self.body


class SendingMessage:
    '''The SendingMessage class declaration.

    Attributes:
        message (Any): The message to send.
    '''

    def __init__(self, message: Any):
        '''The SendingMessage initializer.

        Args:
            message (Any): The message to send.
        '''

        self.message = message

    @property
    def serialized(self) -> bytes:
        '''Serialize the message.

        Returns:
            bytes: The serialized message.
        '''

        # TODO: Do the serialiation process.
        return b'serialized message'
