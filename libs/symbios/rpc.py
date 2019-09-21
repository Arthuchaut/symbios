'''
@desc    The RPC class definition.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-21
@note    0.1.0 (2019-09-21): Writed the first drafts.
'''

from typing import Dict, Callable
from uuid import uuid4

import aiormq

from . import Props
from .message import IncomingMessage, SendingMessage
from .queue import Queue


class RPC:
    '''The RPC class declaration.

    Allows to call the broker and waiting for its response back.

    Attributes:
        symbios (Symbios): A Symbios instance.
        _future (Any): The future response back.
        _ack (bool): Allows to know if the response was sent.
        _cid (str): The correlation id for identify the caller.
        _reply_queue (str): The queue to tell the broker where to reply.
    '''

    def __init__(self, symbios: object):
        '''The RPC initializer.

        Args:
            symbios (Symbios): The symbios instance.
        '''

        self.symbios: object = symbios
        self._futures: Dict[str, Callable] = {}
        self._cid: str = None
        self._reply_queue: str = None

    async def _on_reply(
        self, symbios: object, message: IncomingMessage
    ) -> None:
        '''The task that will be called on the broker response.

        Valorize the self.response attribute with the received message.

        Args:
            message (IncomingMessage): The message from the broker.
        '''

        future: Any = self._futures.pop(self._cid)
        future.set_result(message)

    async def call(
        self, message: SendingMessage, *, routing_key: str
    ) -> IncomingMessage:
        '''The calling procedure.

        Emit a message to the broker and wait for its response back.
        
        Args:
            message (SendingMessage): The message to send.
            routing_key (str): The routing key to emit the message.

        Returns:
            IncomingMessage: The broker response back.
        '''

        self._cid = str(uuid4())
        future: Any = self.symbios.event_loop.create_future()
        self._futures[self._cid] = future

        queue: Queue = Queue(self._cid, exclusive=True, auto_delete=True)

        await self.symbios.declare_queue(queue)
        await self.symbios.listen(
            self._on_reply, queue=queue, ephemeral=True, no_ack=True
        )

        await self.symbios.emit(
            message,
            routing_key=routing_key,
            props=Props(correlation_id=self._cid, reply_to=queue.queue),
        )

        return await future

