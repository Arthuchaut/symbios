'''
@desc    The producer class for emit requests to the broker.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import Awaitable, Any

from . import Props, Channel
from .message import SendingMessage
from .symbios import Symbios
from .exchange import Exchange


class Producer:
    '''The Producer class declaration.

    Allows to emit a message to the borker.

    Attributes:
        symbios (Symbios): The Symbios instance.
        exchange (str): the exchange name to bind with the exchange type.
        exchange_type (str): The exhange type.
        routing_key (str): The message routing key.
        props (Props): The message properties that contain the header.
        mandatory (bool): Tell if the message is important or not.
        immediate (bool): Bypass the exchange type rules and send
            the message to the receiver directly if True.
    '''

    def __init__(
        self,
        *,
        symbios: Symbios,
        exchange: Exchange = Exchange(),
        routing_key: str = None,
        props: Props = Props(),
        mandatory: bool = False,
        immediate: bool = False,
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
        '''

        self.symbios: Symbios = symbios
        self.exchange: Exchange = exchange
        self.routing_key: str = routing_key
        self.props: Props = props
        self.mandatory: bool = mandatory
        self.immediate: bool = immediate

    async def emit(self, message: SendingMessage) -> None:
        '''Emit a message to the broker.

        Important: Make sure that the destination queue(s) are correctly 
        declared by a Consumer before sending a message.

        Args:
            message (SendingMessage): The message to send.

        Raises:
            ProducerError: If the type of exchange requires a routing_key.
        '''

        chann: Channel = await self.symbios.connector.channel

        if self.exchange.exchange != '' and self.exchange.exchange is not None:
            await chann.exchange_declare(**self.exchange.__dict__)

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

        await chann.basic_publish(
            message.serialized,
            routing_key=self.routing_key,
            exchange=self.exchange.exchange,
            properties=self.props,
            immediate=self.immediate,
            mandatory=self.mandatory,
        )


class ProducerError(Exception):
    '''The ProducerError Exception class.
    '''

    def __init__(self, message: str):
        super().__init__(message)
