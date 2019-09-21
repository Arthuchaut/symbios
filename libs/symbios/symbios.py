'''
@desc    The main class of the Symbios library.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import Dict, Union

from . import Props
from .connector import Connector
from .consumer import Consumer
from .producer import Producer
from .queue import Queue
from .exchange import Exchange
from .message import IncomingMessage, SendingMessage
from .middleware import Middleware, MiddlewareQueue


class Symbios(Connector):
    '''The Symbios class declaration.

    Allows to communicate with the broker.

    Attributes:
        middleware_queue (MiddlewareQueue): The middleware queue.
    '''

    def __init__(self, **kwargs: Dict[str, Union[str, int]]):
        '''The Symbios initializer.

        Args:
            **kwargs (Dict[str, Union[str, int]]): The connection credentials.
                See the Connector __init__ documentation for more information.
        '''

        ...

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

        ...

    async def listen(
        self,
        task: Callable[[Symbios, IncomingMessage], Awaitable[Any]],
        *,
        queue: Queue = Queue(),
        no_ack: bool = False,
        exclusive: bool = False,
        arguments: ArgumentsType = None,
        consumer_tag: str = None,
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
        '''

        ...

    async def call(
        self,
        message: SendingMessage,
        *,
        exchange: Exchange = Exchange(),
        routing_key: str = None,
    ) -> Union[str, Dict[str, Any]]:
        '''An RPC communication pattern.

        Emit a message to the broker and retrieve the response.

        Args:
            message (SendingMessage): The message to send.
            exchange (Exchange): the exchange name to bind with the 
                exchange type. Default to Exchange().
            routing_key (str): The message routing key. Default to None.

        Returns:
            Union[str, Dict[str, Any]]: The broker response back.
        '''

        ...

    def use(self, midd: Middleware) -> None:
        '''Implement a new middleware for the consumer.

        All middlewares will be called before the main task.
        The IncomingMessage could be modified in.

        Args:
            midd (Middleware): The middleware to append to the queue.
        '''

        ...
