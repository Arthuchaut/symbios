'''
@desc    The producer class for emit requests to the broker.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import Awaitable, Any

from . import Connector, Props, SendingMessage, Channel


class Producer:
    '''The Producer class declaration.

    Allows to emit a message to the borker.

    Attributes:
        DIRECT_EXCHANGE (str): The default exhange type. Sends the message
            to alls the queues that are bound to the same routing_key that
            the message routing_key.

            Example: 
                If Producer::routing_key == Consumer::queue::binding_key
                then deliver the message to this queue.
        FANOUT_EXCHANGE (str): Sends the message to all the queues 
            that are bound to it. The routing_key will be ignored.

            Example:
                If Consumer::binding_key is bound to this exchange_type
                then deliver the message to this queue.
        TOPIC_EXCHANGE (str): Sends the message to all the queues that
            are bound to the same routing_key that the message routing_key
            and that the routing_key pattern of the bound queue is matching 
            with the message routing_key.

            Example:
                Producer::routing_key = 'my.routing.key'
                Consumer::binding_key = 'my.*.key'

                is_matching(Producer::routing_key, Consumer::binding_key)
                >>> True

                Producer::routing_key = 'his.routing.key'
                Consumer::binding_key = 'my.*.key'

                is_matching(Producer::routing_key, Consumer::binding_key)
                >>> False
        HEADERS_EXCHANGE (str): Sends the message to all queues at which 
            their routing_key matches to specific header attributes. 
            The routing_key is ignored.

            Example:
                Header::attr['x-match'] = 'my_value'
                Consumer::binding_key = 'my_value'

                Header::attr['x-match'] == Consumer::binding_key
                >>> True

                Header::attr['x-match'] = 'my_other_value'
                Consumer::binding_key = 'my_value'

                Header::attr['x-match'] == Consumer::binding_key
                >>> False
        connector (Connector): The Connector instance.
        exchange (str): the exchange name to bind with the exchange type.
        exchange_type (str): The exhange type.
        routing_key (str): The message routing key.
        props (Props): The message properties that contain the header.
        mandatory (bool): Tell if the message is important or not.
        immediate (bool): Bypass the exchange type rules and send
            the message to the receiver directly if True.
    '''

    DIRECT_EXCHANGE: str = 'direct'
    FANOUT_EXCHANGE: str = 'fanout'
    TOPIC_EXCHANGE: str = 'topic'
    HEADERS_EXCHANGE: str = 'match'

    def __init__(
        self,
        *,
        connector: Connector,
        exchange: str = '',
        exchange_type: str = DIRECT_EXCHANGE,
        routing_key: str = None,
        props: Props = Props(),
        mandatory: bool = False,
        immediate: bool = False,
    ):
        '''The Producer initializer.

        Args:
            connector (Connector): The Connector instance.
            exchange (str): the exchange name to bind with the exchange type.
                Default to ''.
            exchange_type (str): The exhange type. Default to DIRECT_EXCHANGE.
            routing_key (str): The message routing key. Default to None.
            props (Props): The message properties that contain the header.
                Default to an empty instance of Props.
            mandatory (bool): Tell if the message is important or not.
                Default to False.
            immediate (bool): Bypass the exchange type rules and send
                the message to the receiver directly if True.
                Default to False.
        '''

        self.connector: Connector = connector
        self.exchange: str = exchange
        self.exchange_type: str = exchange_type
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

        chann: Channel = await self.connector.channel

        if self.exchange != '' and self.exchange is not None:
            await chann.exchange_declare(
                exchange=self.exchange, exchange_type=self.exchange_type
            )

        if not self.exchange_type in [
            Producer.FANOUT_EXCHANGE,
            Producer.HEADERS_EXCHANGE,
        ] and (self.routing_key == '' or self.routing_key is None):
            raise ProducerError(
                f'Exchange type {self.exchange_type} require a routing_key.'
            )

        await chann.basic_publish(
            message.serialized,
            routing_key=self.routing_key,
            exchange=self.exchange,
            properties=self.props,
            immediate=self.immediate,
            mandatory=self.mandatory,
        )


class ProducerError(Exception):
    '''The ProducerError Exception class.
    '''

    def __init__(self, message: str):
        super().__init__(message)
