'''
@desc    The main class of the Symbios library.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.3.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
@note    0.2.0 (2019-09-21): Implemented the class methods.
@note    0.3.0 (2019-09-22): Implemented some basic middlewares.
'''

from typing import Dict, Union, Callable, Awaitable, Any

from .utils import Props, ArgumentsType, Channel
from .connector import Connector
from .queue import Queue
from .exchange import Exchange
from .message import IncomingMessage, SendingMessage
from .middleware import MiddlewareLibrary, MiddlewareABC, Event
from .producer import Producer
from .consumer import Consumer
from .rpc import RPC

from middlewares.deserializer_middleware import DeserializerMiddleware
from middlewares.serializer_middleware import SerializerMiddleware
from .confirmation import EmitACK, ListenACK, ExchangeACK, QueueACK


class Symbios(Connector):
    '''The Symbios class declaration.

    Allows to communicate with the broker.

    Attributes:
        _midd_library (MiddlewareLibrary): The middleware library.
        rpc (RPC): The RPC instance.
    '''

    def __init__(self, **kwargs: Dict[str, Union[str, int]]):
        '''The Symbios initializer.

        Args:
            **kwargs (Dict[str, Union[str, int]]): The connection credentials.
                See the Connector __init__ documentation for more information.
        '''

        super().__init__(**kwargs)

        self._midd_library: MiddlewareLibrary = MiddlewareLibrary()
        self.rpc: RPC = RPC(self)
        self._init_standard_middlewares()

    def _init_standard_middlewares(self) -> None:
        '''Implement some basic middlewares.
        '''

        self.use(SerializerMiddleware(Event.ON_EMIT))
        self.use(DeserializerMiddleware(Event.ON_LISTEN))

    async def declare_queue(self, queue: Queue) -> QueueACK:
        '''Declare a queue to the broker.

        Args:
            queue (Queue): The queue to declare

        Returns:
            QueueACK: The validation of the declaration.
        '''

        chan: Channel = await self.channel

        confirmation = await chan.queue_declare(**queue.__dict__)

        return QueueACK(confirmation)

    async def declare_exchange(self, exchange: Exchange) -> ExchangeACK:
        '''Declare an exchange to the broker.

        Args:
            exchange (Exchange): The exchange to declare

        Returns:
            ExchangeACK: The validation of the declaration.
        '''

        chan: Channel = await self.channel

        confirmation = await chan.exchange_declare(**exchange.__dict__)

        return ExchangeACK(confirmation)

    async def emit(
        self,
        message: SendingMessage,
        *,
        exchange: Exchange = Exchange(),
        routing_key: str = None,
        props: Props = Props(),
        mandatory: bool = False,
        immediate: bool = False,
    ) -> None:
        '''Emit a message to the broker.

        Args:
            message (SendingMessage): The message to send.
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

        producer: Producer = Producer(
            symbios=self,
            exchange=exchange,
            routing_key=routing_key,
            props=props,
            mandatory=mandatory,
            immediate=immediate,
            midd_library=self._midd_library,
        )

        return await producer.emit(message)

    async def listen(
        self,
        task: Callable[[object, IncomingMessage], None],
        *,
        queue: Queue = Queue(),
        no_ack: bool = False,
        exclusive: bool = False,
        arguments: ArgumentsType = None,
        consumer_tag: str = None,
    ) -> None:
        '''Listen a message from a broker queue.

        Args:
            task (Callable[[Symbios, IncomingMessage], None]): The
                task to call when a message arrives.
            queue (str): The queue to consume. Default to Queue().
            no_ack (bool): If deliver an aknowlegment or not. 
                Default to False.
            exclusive (bool): Only one consumer registered to 
                the targeted queue. Default to False.
            arguments (ArgumentsType): Some properties to the consumer.
                Default to None.
            consumer_tag (str): The consumer identity. Default to None.
        '''

        consumer: Consumer = Consumer(
            symbios=self,
            queue=queue,
            no_ack=no_ack,
            exclusive=exclusive,
            arguments=arguments,
            consumer_tag=consumer_tag,
            midd_library=self._midd_library,
        )

        return await consumer.listen(task)

    def use(self, midd: MiddlewareABC) -> None:
        '''Implement a new middleware for the consumer.

        All middlewares will be called before the main task.
        The IncomingMessage could be modified in.

        Args:
            midd (MiddlewareABC): The middleware instance to register to the
                middleware library.
        '''

        self._midd_library.append(midd)
