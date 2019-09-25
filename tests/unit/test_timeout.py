'''
@desc    The Timeout test class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-25
@note    0.1.0 Writing the first drafts.
'''

import asyncio
from asyncio import CancelledError
from time import time

import pytest

from libs.symbios.timeout import Timeout, TimeoutElapsed


class TestTimeout:
    '''The Timeout tests class.
    '''

    def test_start(self, run_async) -> None:
        '''Test the Timeout.start method.
        '''

        async def test() -> None:
            timeout: Timeout = Timeout()
            t_limit: int = 1

            with pytest.raises(TimeoutElapsed):
                await timeout.start(t_limit)

            timeout._loop.create_task(timeout.start(t_limit))
            timeout.stop()

        run_async(test)

    def test__start_countdown(self, run_async) -> None:
        '''Test the Timeout._start_countdown method.
        '''

        async def test() -> None:
            t_sleep: int = 2

            timeout: Timeout = Timeout()

            t_1: float = time()
            await timeout._start_countdown(t_sleep)
            t_2: float = time()

            assert t_sleep == int(t_2 - t_1)

        run_async(test)

    def test_stop(self, run_async) -> None:
        '''Test the Timeout.stop method.
        '''

        async def test() -> None:
            timeout: Timeout = Timeout()
            t_limit: int = 5

            timeout._loop.create_task(timeout.start(t_limit))
            await asyncio.sleep(1)

            with pytest.raises(CancelledError):
                timeout.stop()
                await timeout._task

        run_async(test)
