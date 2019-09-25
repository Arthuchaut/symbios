from typing import Dict, List, Callable, Any
from collections import namedtuple
import asyncio

import pytest

from libs.symbios import Symbios, Props, ArgumentsType
from libs.symbios.queue import Queue
from libs.symbios.exchange import Exchange
from libs.symbios.message import SendingMessage, IncomingMessage
from libs.symbios.confirmation import QueueACK, EmitACK, ExchangeACK, ListenACK


class MockSymbios:
    '''The Symbios class modifier.

    Modify the Symbios.emit and Symbios.listen methods
    for simulating a basic broker communication.
    '''

    def __init__(self, symbios: Symbios):
        self.symbios: Symbios = symbios
        setattr(self.symbios, '_queue_state', {})

    async def declare_queue(self, *args) -> Any:
        await asyncio.sleep(0.5)
        return 'OK'

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
        '''Modify the Symbios.emit method.
        '''

        if not routing_key in self.symbios._queue_state.keys():
            self.symbios._queue_state[routing_key] = []

        HeaderModel = namedtuple('HeaderModel', 'properties')
        DeliveredMessageModel = namedtuple(
            'DeliveredMessageModel', 'delivery, header, body'
        )

        self.symbios._queue_state[routing_key].append(
            IncomingMessage(
                DeliveredMessageModel(None, HeaderModel(props), message.body)
            )
        )

        await asyncio.sleep(0.5)

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
        '''Modify the Symbios.listen method.
        '''

        async def process_listener() -> None:
            while True:
                try:
                    message: IncomingMessage = self.symbios._queue_state[
                        queue.queue
                    ].pop()

                    while message:
                        await task(self, message)
                        message = self.symbios._queue_state[queue.queue].pop()
                except (KeyError, IndexError):
                    pass

                await asyncio.sleep(0.2)

        self.symbios.event_loop.create_task(process_listener())


class MockChannel:
    '''The aiormq Channel mock class. 
    '''

    async def queue_declare(self, **kwargs) -> Any:
        '''Just return an ack.
        '''

        return 'OK'

    async def basic_publish(self, *args, **kwargs) -> Any:
        '''Just return an ack.
        '''

        return 'OK'
