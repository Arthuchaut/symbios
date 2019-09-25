'''
@desc    The Symbios test class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-25
@note    0.1.0 Writing the first drafts.
'''

from typing import Union

import pytest

from libs.symbios import Symbios, Props
from libs.symbios.queue import Queue
from libs.symbios.exchange import Exchange
from libs.symbios.middleware import MiddlewareABC, Event
from libs.symbios.confirmation import ExchangeACK, QueueACK, EmitACK, ListenACK
from libs.symbios.message import SendingMessage, IncomingMessage

from middlewares import DeserializerMiddleware, SerializerMiddleware


class TestSymbios:
    '''The Symbios test class.
    '''

    def test__init_standard_middlewares(self, symbios: Symbios) -> None:
        '''Test the standard middleware initialization.
        '''

        assert isinstance(
            symbios._midd_library._library[Event.ON_EMIT][0],
            SerializerMiddleware,
        )

        assert isinstance(
            symbios._midd_library._library[Event.ON_LISTEN][0],
            DeserializerMiddleware,
        )

    def test_declare_queue(self, symbios: Symbios, run_async) -> None:
        '''Test the queue declaration.
        '''

        async def test() -> None:
            ack: QueueACK = await symbios.declare_queue(Queue('symbios_tests'))
            assert isinstance(ack, QueueACK)

            with pytest.raises(TypeError):
                await symbios.declare_queue(Queue(42))

        run_async(test)

    def test_declare_exchange(self, symbios: Symbios, run_async) -> None:
        '''Test the exchange declaration.
        '''

        async def test() -> None:
            ack: ExchangeACK = await symbios.declare_exchange(
                Exchange('symbios_tests')
            )
            assert isinstance(ack, ExchangeACK)

            ack: ExchangeACK = await symbios.declare_exchange(Exchange(42))
            assert isinstance(ack, ExchangeACK)

            ack: ExchangeACK = await symbios.declare_exchange(Exchange(3.14))
            assert isinstance(ack, ExchangeACK)

        run_async(test)

    def test_emit(self, symbios: Symbios, mocked_channel, run_async) -> None:
        '''Test the Symbios.emit method.
        '''

        async def test() -> None:
            mocked_channel(await symbios.channel)

            message: SendingMessage = SendingMessage('Lapin')
            ack: EmitACK = await symbios.emit(
                message, routing_key='symbios_tests'
            )

            assert isinstance(ack, EmitACK)

        run_async(test)

    def test_listen(self, symbios: Symbios, run_async) -> None:
        '''Test the Symbios.listen method.
        '''

        async def test() -> None:
            async def listen_handler(
                sym_sock, message: IncomingMessage
            ) -> None:
                ...

            queue: Queue = Queue('symbios_tests')
            ack: ListenACK = await symbios.listen(
                listen_handler, queue=queue, no_ack=True
            )

            assert isinstance(ack, ListenACK)

        run_async(test)

    def test_use(self, symbios: Symbios) -> None:
        '''Test the middleware stacking.
        '''

        class MiddlewareTest(MiddlewareABC):
            async def execute(
                self,
                symbios: Symbios,
                message: Union[IncomingMessage, SendingMessage],
            ) -> None:
                ...

        symbios.use(MiddlewareTest(Event.ON_EMIT))
        symbios.use(MiddlewareTest(Event.ON_LISTEN))

        for midds in symbios._midd_library._library.values():
            for midd in midds:
                assert isinstance(midd, MiddlewareABC)
