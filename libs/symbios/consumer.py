'''
@desc    The consumer class for listen message from the broker.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

from typing import Callable, Awaitable, Any

from . import Channel, DeliveredMessage, ArgumentsType
from .message import IncomingMessage
from .symbios import Symbios
from .queue import Queue


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
        task (Callable[[Symbios, IncomingMessage], Awaitable[Any]]): The task
            to call when a message arrives.
        declare_ok (Any): The future of the declared queue.
        consume_ok (Any): The future of the consumed queue.
    '''

    def __init__(
        self,
        *,
        symbios: Symbios,
        queue: Queue = Queue(),
        no_ack: bool = False,
        exclusive: bool = False,
        arguments: ArgumentsType = None,
        consumer_tag: str = None
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
        '''

        self.symbios: Symbios = symbios
        self.queue: Queue = queue
        self.no_ack: bool = no_ack
        self.exclusive: bool = exclusive
        self.arguments: ArgumentsType = arguments
        self.consumer_tag: str = consumer_tag
        self.task: Callable[[Symbios, IncomingMessage], Awaitable[Any]] = None
        self.declare_ok: Any = None
        self.consume_ok: Any = None

    async def listen(
        self, task: Callable[[Symbios, IncomingMessage], Awaitable[Any]]
    ) -> None:
        '''Listen a queue.

        Args:
            task (Callable[[Symbios, IncomingMessage], Awaitable[Any]]): The
                task to call when a message arrives.
        '''

        self.task = task
        chann: Channel = await self.symbios.channel

        self.declare_ok = await chann.queue_declare(**self.queue.__dict__)

        self.consume_ok = await chann.basic_consume(
            self.declare_ok.queue,
            self._embed,
            no_ack=self.no_ack,
            exclusive=self.exclusive,
            arguments=self.arguments,
            consumer_tag=self.consumer_tag,
        )

    async def _embed(self, message: DeliveredMessage) -> Awaitable[Any]:
        '''Embed the task with the Symbios parameters.

        Call the task.

        Args:
            message (DeliveredMessage): The aiormq message model.
        '''

        message: IncomingMessage = IncomingMessage(message)

        await self.task(self.symbios, message)
