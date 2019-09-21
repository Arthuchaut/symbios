'''
@desc    The RPC class definition.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-21
@note    0.1.0 (2019-09-21): Writed the first drafts.
'''

from .message import IncomingMessage, SendingMessage


class RPC:
    '''The RPC class declaration.

    Allows to call the broker and waiting for its response back.

    Attributes:
        symbios (Symbios): A Symbios instance.
        response (IncomingMessage): The broker response back.
        _ack (bool): Allows to know if the response was sent.
        _cid (str): The correlation id for identify the caller.
        _reply_queue (str): The queue to tell the broker where to reply.
    '''

    def __init__(self, symbios: object):
        '''The RPC initializer.

        Args:
            symbios (Symbios): The symbios instance.
        '''

        ...

    async def _on_reply(self, message: IncomingMessage) -> None:
        '''The task that will be called on the broker response.

        Args:
            message (IncomingMessage): The message from the broker.
        '''

        ...

    async def call(
        self, message: SendingMessage, *, routing_key: str
    ) -> IncomingMessage:
        '''The calling procedure.

        Emit a message to the brokler and wait for its response back.
        
        Args:
            message (SendingMessage): The message to send.
            routing_key (str): The routing key to emit the message.

        Returns:
            IncomingMessage: The broker response back.
        '''

        ...
