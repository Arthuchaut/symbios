'''
@desc    The RPC class definition.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-21
@note    0.1.0 (2019-09-21): Writed the first drafts.
'''

from typing import Dict, Callable, List
from uuid import uuid4
from asyncio import Task, Future

import aiormq

from .utils import Props
from .message import IncomingMessage, SendingMessage
from .queue import Queue
from .timeout import Timeout


class RPC:
    '''The RPC class declaration.

    Allows to call the broker and waiting for its response back.

    Attributes:
        symbios (Symbios): A Symbios instance.
        _future (Future): The future response back.
        _ack (bool): Allows to know if the response was sent.
        _reply_queue (str): The queue to tell the broker where to reply.
    '''

    def __init__(self, symbios: object):
        '''The RPC initializer.

        Args:
            symbios (Symbios): The symbios instance.
        '''

        self.symbios: object = symbios
        self._futures: Dict[str, Future] = {}
        self._reply_queue: str = None

    async def _on_reply(
        self, symbios: object, message: IncomingMessage
    ) -> None:
        '''The task that will be called on the broker response.

        Valorize the self.response attribute with the received message.

        Args:
            message (IncomingMessage): The message from the broker.
        '''

        try:
            future, countdown = self._futures.pop(message.props.correlation_id)

            countdown.stop()
            future.set_result(message)
        except Exception as e:
            raise RPCError(f'Expected a correlation_id from the server.')

    async def call(
        self, message: SendingMessage, *, routing_key: str, timeout: int = None
    ) -> IncomingMessage:
        '''The calling procedure.

        Emit a message to the broker and wait for its response back.
        
        Args:
            message (SendingMessage): The message to send.
            routing_key (str): The routing key to emit the message.
            timeout (int): The time limite (in second) for the timeout.
                Raised a TimeoutElapsed exception if the countdown has
                expired. Default to None.

        Returns:
            IncomingMessage: The broker response back.
        '''

        cid: str = str(uuid4())
        countdown: Timeout = Timeout(self.symbios.event_loop)
        future: Future = self.symbios.event_loop.create_future()

        self._futures[cid] = (future, countdown)

        queue: Queue = Queue(cid, auto_delete=True)

        await self.symbios.declare_queue(queue)
        await self.symbios.listen(self._on_reply, queue=queue, no_ack=True)

        await self.symbios.emit(
            message,
            routing_key=routing_key,
            props=Props(correlation_id=cid, reply_to=queue.queue),
        )

        if timeout:
            await countdown.start(timeout)

        return await future

    def multi_calls(self, calls: List[call]) -> List[Task]:
        '''Process multi asynchronous RPC.

        Args:
            calls (List[RPC.call]): The list of RPC.call.

        Returns:
            List[Task]: The asyncio.Task list created from calls.
        '''

        task_queue: List[Task] = []

        for call in calls:
            task_queue.append(self.symbios.event_loop.create_task(call))

        return task_queue


class RPCError(Exception):
    '''The RPCError exception class.
    '''

