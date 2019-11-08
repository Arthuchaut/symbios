'''
@desc    The timeout class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-23
@note    0.1.0 (2019-09-23): Writed the first drafts.
'''

import asyncio
from asyncio import AbstractEventLoop, Task, CancelledError


class Timeout:
    '''The Timeout class declaration.

    Allows to define a delay and raise a TimeoutElapsed exception
    if the countdown expire.

    Attributes:
        _loop (AbstractEventLoop): The asyncio event loop.
        _task (Task): A coroutine that process the countdown.
    '''

    def __init__(
        self, loop: AbstractEventLoop = asyncio.get_event_loop()
    ) -> None:
        '''The Timeout initializer.

        Args:
            _loop (AbstractEventLoop): The asyncio event loop.
                Default to a new event loop.
        '''

        self._loop: AbstractEventLoop = loop
        self._task: Task = None

    async def start(self, limit: int) -> None:
        '''Start the countdown.

        Create a task that start the countdown.
        Raise an exception if the task has ended.
        Return None if the task is cancelled.

        Raises:
            TimeoutElapsed: If the countdown expire.

        Args:
            limit (int): The countdown limit.
        '''

        self._task = self._loop.create_task(self._start_countdown(limit))

        try:
            await self._task
        except CancelledError:
            return

        raise TimeoutElapsed()

    async def _start_countdown(self, limit: int) -> None:
        '''A coroutine that await for n time (in seconds).

        Args:
            limit (int): The countdown limit.            
        '''

        await asyncio.sleep(limit)

    def stop(self) -> None:
        '''Cancel the self._start_countdown cotourine.
        '''

        if self._task and not self._task.done():
            self._task.cancel()


class TimeoutElapsed(Exception):
    '''The TimeoutElapsed Exception.

    Raised when the timeout had expired.
    '''

