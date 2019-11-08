'''
@desc    The producer class for emit requests to the broker.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import Awaitable, Any, Dict

from .utils import Props, Channel
from .message import SendingMessage
from .exchange import Exchange
from .middleware import MiddlewareLibrary, Event
from .confirmation import EmitACK, ExchangeACK


class Producer:
    '''The Producer class declaration.

    Allows to emit a message to the borker.

    Attributes:
        _CONTENT_TYPES (Dict[Any, str]): The association of types 
            with their content-type.
        symbios (Symbios): The Symbios instance.
        exchange (str): the exchange name to bind with the exchange type.
        exchange_type (str): The exhange type.
        routing_key (str): The message routing key.
        props (Props): The message properties that contain the header.
        mandatory (bool): Tell if the message is important or not.
        immediate (bool): Bypass the exchange type rules and send
            the message to the receiver directly if True.
        _midd_library (MiddlewareLibrary): The Symbios middleware library.        
    '''

    _CONTENT_TYPES: Dict[Any, str] = {
        str: 'text/plain',
        bool: 'text/plain',
        int: 'text/plain',
        float: 'text/plain',
        dict: 'application/json',
    }

    def __init__(
        self,
        *,
        symbios: object,
        exchange: Exchange = Exchange(),
        routing_key: str = None,
        props: Props = Props(),
        mandatory: bool = False,
        immediate: bool = False,
        midd_library: MiddlewareLibrary,
    ):
        '''The Producer initializer.

        Args:
            symbios (Symbios): The Symbios instance.
            exchange (Exchange): the exchange name to bind with the 
                exchange type. Default to Exchange().
            routing_key (str): The message routing key. Default to None.
            props (Props): The message properties that contain the header.
                Default to an empty instance of Props.
            mandatory (bool): Tell if the message is important or not.
                Default to False.
            immediate (bool): Bypass the exchange type rules and send
                the message to the receiver directly if True.
                Default to False.
            _midd_library (MiddlewareLibrary): The Symbios middleware library.    
        '''

        self.symbios: object = symbios
        self.exchange: Exchange = exchange
        self.routing_key: str = routing_key
        self.props: Props = props
        self.mandatory: bool = mandatory
        self.immediate: bool = immediate
        self.declare_ok: object = None
        self.produce_ok: object = None
        self._midd_library: MiddlewareLibrary = midd_library

    async def emit(self, message: SendingMessage) -> EmitACK:
        '''Emit a message to the broker.

        Important: Make sure that the destination queue(s) are correctly 
        declared by a Consumer before sending a message.
        Call all associated middlewares before emit the message.

        Args:
            message (SendingMessage): The message to send.

        Raises:
            ProducerError: If the type of exchange requires a routing_key.

        Returns:
            EmitACK: The producer confirmation.
        '''

        chann: Channel = await self.symbios.channel

        if self.exchange.exchange != '' and self.exchange.exchange is not None:
            declare_ok = await chann.exchange_declare(**self.exchange.__dict__)
            self.declare_ok = ExchangeACK(declare_ok)

        if not self.exchange.exchange_type in [
            Exchange.FANOUT,
            Exchange.HEADERS,
        ] and (self.routing_key == '' or self.routing_key is None):
            raise ProducerError(
                (
                    f'Exchange type {self.exchange.exchange_type} '
                    f'require a routing_key.'
                )
            )

        if not self.props.content_type:
            self.props.content_type = self._determine_content_type(message)

        if not self._midd_library is None:
            await self._midd_library.run_until_end(
                self.symbios, message, Event.ON_EMIT
            )

        produce_ok = await chann.basic_publish(
            message.serialized,
            routing_key=self.routing_key,
            exchange=self.exchange.exchange,
            properties=self.props,
            immediate=self.immediate,
            mandatory=self.mandatory,
        )

        self.produce_ok = EmitACK(produce_ok)

        return self.produce_ok

    def _determine_content_type(self, message: SendingMessage) -> str:
        '''Try to determine the content-type via the message type.

        Args:
            message (SendingMessage): The message to send.

        Returns:
            str: The content_type retreived or ''.
        '''

        content_type: str = ''

        try:
            content_type = Producer._CONTENT_TYPES[type(message.body)]
        except KeyError as e:
            pass

        return content_type


class ProducerError(Exception):
    '''The ProducerError Exception class.
    '''

    def __init__(self, message: str):
        super().__init__(message)
