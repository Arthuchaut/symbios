'''
@desc    The main class of the Symbios library.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.2.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
@note    0.2.0 (2019-09-21): Implemented the class methods.
'''

from typing import Dict, Union, Callable, Awaitable, Any

from . import Props, ArgumentsType, Channel, GetEmpty, GetOk
from .connector import Connector
from .queue import Queue
from .exchange import Exchange
from .message import IncomingMessage, SendingMessage
from .middleware import Middleware, MiddlewareQueue
from .producer import Producer
from .consumer import Consumer
from .rpc import RPC


class Symbios(Connector):
    '''The Symbios class declaration.

    Allows to communicate with the broker.

    Attributes:
        _middleware_queue (MiddlewareQueue): The middleware queue.
    '''

    def __init__(self, **kwargs: Dict[str, Union[str, int]]):
        '''The Symbios initializer.

        Args:
            **kwargs (Dict[str, Union[str, int]]): The connection credentials.
                See the Connector __init__ documentation for more information.
        '''

        super().__init__(**kwargs)

        self._middleware_queue: MiddlewareQueue = MiddlewareQueue()
        self.rpc: RPC = RPC(self)

    async def declare_queue(self, queue: Queue) -> Union[GetEmpty, GetOk]:
        '''Declare a queue to the broker.

        Args:
            queue (Queue): The queue to declare

        Returns:
            Union[GetEmpty, GetOk]: The validation of the declaration.
        '''

        chan: Channel = await self.channel

        return await chan.queue_declare(**queue.__dict__)

    async def declare_exchange(
        self, exhange: Exchange
    ) -> Union[GetEmpty, GetOk]:
        '''Declare an exchange to the broker.

        Args:
            exhange (Exchange): The exchange to declare

        Returns:
            Union[GetEmpty, GetOk]: The validation of the declaration.
        '''

        chan: Channel = await self.channel

        return await chan.exchange_declare(**exchange.__dict__)

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
        )

        await producer.emit(message)

    async def listen(
        self,
        task: Callable[[object, IncomingMessage], Awaitable[Any]],
        *,
        queue: Queue = Queue(),
        no_ack: bool = False,
        exclusive: bool = False,
        arguments: ArgumentsType = None,
        consumer_tag: str = None,
        ephemeral: bool = False,
    ) -> None:
        '''Listen a message from a broker queue.

        Args:
            task (Callable[[Symbios, IncomingMessage], Awaitable[Any]]): The
                task to call when a message arrives.
            queue (str): The queue to consume. Default to Queue().
            no_ack (bool): If deliver an aknowlegment or not. 
                Default to False.
            exclusive (bool): Only one consumer registered to 
                the targeted queue. Default to False.
            arguments (ArgumentsType): Some properties to the consumer.
                Default to None.
            consumer_tag (str): The consumer identity. Default to None.
            ephemeral (bool): If the listener is ephemeral or not.
                If True, the listener will be deleted to the middleware
                stack after the consuming. Default to False.
        '''

        midd: Middleware = Middleware(task, ephemeral=ephemeral)
        self._middleware_queue.append(midd)

        consumer: Consumer = Consumer(
            symbios=self,
            queue=queue,
            no_ack=no_ack,
            exclusive=exclusive,
            arguments=arguments,
            consumer_tag=consumer_tag,
        )

        await consumer.listen(self._middleware_queue.run_until_end)

    def use(self, midd: Middleware) -> None:
        '''Implement a new middleware for the consumer.

        All middlewares will be called before the main task.
        The IncomingMessage could be modified in.

        Args:
            midd (Middleware): The middleware to append to the queue.
        '''

        self._middleware_queue.append(midd)
