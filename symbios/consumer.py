'''
@desc    The consumer class for listen message from the broker.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

import asyncio

from typing import Callable, Awaitable, Any

from .utils import Channel, DeliveredMessage, ArgumentsType
from .message import IncomingMessage
from .queue import Queue
from .middleware import MiddlewareLibrary, Event
from .confirmation import ListenACK, QueueACK


class Consumer:
    '''The Consumer class declaration.

    Listen message from the broker.

    Attributes:
        symbios (Symbios): The Symbios instance.
        queue (str): The queue to consume.
        no_ack (bool): If deliver an aknowlegment or not.
        exclusive (bool): Only one consumer registered to the targeted queue.
        arguments (ArgumentsType): Some properties to the consumer.
        consumer_tag (str): The consumer identity.
        task (Callable[[Symbios, IncomingMessage], None]): 
            The task to call when a message arrives.
        declare_ok (Any): The future of the declared queue.
        consume_ok (Any): The future of the consumed queue.
        _midd_library (MiddlewareLibrary): The Symbios middleware library.
    '''

    def __init__(
        self,
        *,
        symbios: object,
        queue: Queue = Queue(),
        no_ack: bool = False,
        exclusive: bool = False,
        arguments: ArgumentsType = None,
        consumer_tag: str = None,
        midd_library: MiddlewareLibrary,
    ):
        '''The Consumer initializer.

        Args:
            symbios (Symbios): The Symbios instance.
            queue (str): The queue to consume. Default to Queue().
            no_ack (bool): If deliver an aknowlegment or not. 
                Default to False.
            exclusive (bool): Only one consumer registered to 
                the targeted queue. Default to False.
            arguments (ArgumentsType): Some properties to the consumer.
                Default to None.
            consumer_tag (str): The consumer identity. Default to None.
            midd_library (MiddlewareLibrary): The Symbios middleware library.
        '''

        self.symbios: object = symbios
        self.queue: Queue = queue
        self.no_ack: bool = no_ack
        self.exclusive: bool = exclusive
        self.arguments: ArgumentsType = arguments
        self.consumer_tag: str = consumer_tag
        self.task: Callable[[object, IncomingMessage], None] = None
        self.declare_ok: Any = None
        self.consume_ok: Any = None
        self._midd_library = midd_library

    async def listen(
        self, task: Callable[[object, IncomingMessage], None]
    ) -> ListenACK:
        '''Listen a queue.

        Args:
            task (Callable[[Symbios, IncomingMessage], None]): 
                The task to call when a message arrives.

        Returns:
            ListenACK: The consumer confirmation.
        '''

        self.task = task
        chann: Channel = await self.symbios.channel

        declare_ok = await chann.queue_declare(**self.queue.__dict__)
        self.declare_ok = QueueACK(declare_ok)

        consume_ok = await chann.basic_consume(
            self.declare_ok.confirmation.queue,
            self._embed,
            no_ack=self.no_ack,
            exclusive=self.exclusive,
            arguments=self.arguments,
            consumer_tag=self.consumer_tag,
        )

        self.consume_ok = ListenACK(consume_ok)

        return self.consume_ok

    async def _embed(self, message: DeliveredMessage) -> None:
        '''Embed the task with the Symbios parameters.
        
        Call the associated middlewares and then call the task.

        Args:
            message (DeliveredMessage): The aiormq message model.
        '''

        message: IncomingMessage = IncomingMessage(message)

        if not self._midd_library is None:
            await self._midd_library.run_until_end(
                self.symbios, message, Event.ON_LISTEN
            )

        await self.task(self.symbios, message)
