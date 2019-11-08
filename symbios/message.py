'''
@desc    The message class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.3.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
@note    0.2.0 (2019-09-22): Redesigned message classes since 
                             the new middleware structure.
'''

from typing import Union, Dict, Any
import json

from .utils import DeliveredMessage, GetEmpty, GetOk, Props


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


class SendingMessage:
    '''The SendingMessage class declaration.

    Attributes:
        body (Union[str, Dict[str, Any]]): The message to send.
    '''

    def __init__(self, body: Union[str, Dict[str, Any]]):
        '''The SendingMessage initializer.

        Args:
            body (Union[str, Dict[str, Any]]): The message to send.
        '''

        self.body: Union[str, Dict[str, Any]] = body


class SendingMessageError(Exception):
    '''The SendingMessageError Exception class.
    '''

    def __init__(self, message: str):
        super().__init__(message)
