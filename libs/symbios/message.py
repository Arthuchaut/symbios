'''
@desc    The message class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import Union, Dict, Any
import json

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
        _content_type_corr (Dict[str, Any]): The content type converted 
            dictionnary.
        deserialized (Union[str, Dict[str, Any]]): The deserialized message.
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
        self._content_type_corr: Dict[str, Any] = {
            'text/plain': self._parse_text,
            'application/json': self._parse_json,
        }

    @property
    def deserialized(self) -> Union[str, Dict[str, Any]]:
        '''Return the deserialized message body.

        Returns:
            Union[str, Dict[str, Any]]: The deserialized message.
        '''

        obj: Union[str, Dict[str, Any]] = None

        try:
            obj = self._content_type_corr[self.props.content_type](self.body)
        except KeyError as e:
            obj = self._parse_text(self.body)

        return obj

    def _parse_text(self, body: bytes) -> str:
        '''Parse the body to string.

        Args:
            body (bytes): The message body to parse.

        Returns:
            str: The body parsed.
        '''

        return body.decode()

    def _parse_json(self, body: bytes) -> Dict[str, Any]:
        '''Parse the body to Dict[str, Any].

        Args:
            body (bytes): The message body to parse.

        Returns:
            Dict[str, Any]: The body parsed.
        '''

        return json.loads(self._parse_text(body))


class SendingMessage:
    '''The SendingMessage class declaration.

    Attributes:
        _CONTENT_TYPES (Dict[Any, str]): The content type dictionnary.
        _type_corr (Dict[str, Any]): The typing converter dictionnary.
        message (Union[str, Dict[str, Any]]): The message to send.
        content_type (str): The message content type.
        serialized (bytes): The message converted in bytes.
    '''

    _CONTENT_TYPES: Dict[Any, str] = {
        str: 'text/plain',
        bool: 'text/plain',
        int: 'text/plain',
        float: 'text/plain',
        dict: 'application/json',
    }

    def __init__(self, message: Union[str, Dict[str, Any]]):
        '''The SendingMessage initializer.

        Args:
            message (Union[str, Dict[str, Any]]): The message to send.
        '''

        self.message: Union[str, Dict[str, Any]] = message
        self._type_corr: Dict[str, Any] = {
            str: self._parse_text,
            int: self._parse_text,
            float: self._parse_text,
            dict: self._parse_json,
        }

    @property
    def serialized(self) -> bytes:
        '''Serialize the message.

        Raises:
            SendingMessageError: If the type of message is not serializable.

        Returns:
            bytes: The serialized message.
        '''

        try:
            return self._type_corr[type(self.message)](self.message)
        except KeyError as e:
            raise SendingMessageError(
                f'Type {type(self.message).__name__} is not serializable.'
            )

    @property
    def content_type(self) -> str:
        '''Return the message content type.

        Returns:
            str: The message content type.
        '''

        try:
            return SendingMessage._CONTENT_TYPES[type(self.message)]
        except KeyError as e:
            return ''

    def _parse_text(self, body: Union[str, int, float]) -> bytes:
        '''Parse the body string to bytes.

        Args:
            body (str): The message body to parse.

        Returns:
            bytes: The body parsed.
        '''

        return str(body).encode()

    def _parse_json(self, body: Dict[str, Any]) -> bytes:
        '''Parse the Dict[str, Any] body to a stringify JSON bytes.

        Args:
            body (Dict[str, Any]): The message body to parse.

        Returns:
            bytes: The body parsed.
        '''

        return json.dumps(body).encode()


class SendingMessageError(Exception):
    '''The SendingMessageError Exception class.
    '''

    def __init__(self, message: str):
        super().__init__(message)
