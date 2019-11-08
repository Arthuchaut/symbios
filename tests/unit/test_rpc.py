'''
@desc    The RPC test class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-25
@note    0.1.0 Writing the first drafts.
'''

import asyncio

import pytest

from symbios import Symbios
from symbios.utils import Props
from symbios.message import SendingMessage, IncomingMessage
from symbios.rpc import RPC
from symbios.queue import Queue
from symbios.timeout import Timeout
from .mocks import MockSymbios


class TestRPC:
    def test_call(self, mocked_symbios, init_rpc_server, run_async) -> None:
        '''Test the RPC.call method.
        '''

        async def test() -> None:
            mocked_symbios.event_loop.create_task(
                init_rpc_server(mocked_symbios)
            )

            rpc: RPC = RPC(mocked_symbios)

            res = await rpc.call(
                SendingMessage('HI'), routing_key='symbios_tests'
            )

            assert res.body == 'RPC_ACK'

        run_async(test)

    def test__on_reply(
        self, symbios: Symbios, delivered_message_model, run_async
    ) -> None:
        '''Test the RPC._on_reply method.
        '''

        async def test() -> None:
            fake_uid: str = '1-2-3-4'
            future = symbios.event_loop.create_future()

            rpc: RPC = RPC(symbios)

            rpc._futures[fake_uid] = (future, Timeout(symbios.event_loop))

            await rpc._on_reply(
                symbios,
                IncomingMessage(
                    delivered_message_model(
                        None, Props(correlation_id=fake_uid), 'ON_REPLY_OK'
                    )
                ),
            )

            await future

            assert future.result().body == 'ON_REPLY_OK'

        run_async(test)

    def test_multi_calls(
        self, mocked_symbios, run_async, init_rpc_server
    ) -> None:
        '''Test the RPC.multi_calls method.
        '''

        async def test() -> None:
            mocked_symbios.event_loop.create_task(
                init_rpc_server(mocked_symbios)
            )
            rpc: RPC = RPC(mocked_symbios)

            task_queue = rpc.multi_calls(
                [
                    rpc.call(SendingMessage('HI'), routing_key='symbios_tests')
                    for _ in range(1)
                ]
            )

            for task in task_queue:
                await task
                assert task.result().body == 'RPC_ACK'

        run_async(test)
