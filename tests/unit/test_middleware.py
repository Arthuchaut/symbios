'''
@desc    The middleware test classes.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-25
@note    0.1.0 Writing the first drafts.
'''

from typing import Union

import pytest

from libs.symbios import Symbios
from libs.symbios.message import IncomingMessage, SendingMessage
from libs.symbios.middleware import MiddlewareABC, MiddlewareLibrary, Event


class TestMiddlewareABC:
    '''The MiddlewareABC test class.
    '''

    @pytest.mark.parametrize('event', [Event.ON_EMIT, Event.ON_LISTEN])
    def test_middlewareabc(
        self, delivered_message_model: object, event: int
    ) -> None:
        '''Test the MiddlewareABC implementation.
        '''

        class MiddlewareTest(MiddlewareABC):
            ...

        with pytest.raises(TypeError):
            midd: MiddlewareABC = MiddlewareTest(event)

        class MiddlewareTest(MiddlewareABC):
            async def execute(
                self,
                symbios: Symbios,
                message: Union[IncomingMessage, SendingMessage],
            ) -> None:
                ...

        midd: MiddlewareABC = MiddlewareTest(event)


class TestMiddlewareLibrary:
    '''The MiddlewareLibrary test class.
    '''

    @pytest.mark.parametrize('event', [Event.ON_EMIT, Event.ON_LISTEN])
    def test_append(self, event: int) -> None:
        '''Test the middleware stacking in the middleware library.
        '''

        class MiddlewareTest(MiddlewareABC):
            async def execute(
                self,
                symbios: Symbios,
                message: Union[IncomingMessage, SendingMessage],
            ) -> None:
                ...

        midd_lib: MiddlewareLibrary = MiddlewareLibrary()

        assert not len(midd_lib._library[event])

        midd_lib.append(MiddlewareTest(event))

        assert len(midd_lib._library[event]) == 1

        midd_lib.append(MiddlewareTest(event))

        assert len(midd_lib._library[event]) == 2

    @pytest.mark.parametrize('event', [Event.ON_EMIT, Event.ON_LISTEN])
    def test_run_until_end(self, run_async, event: int) -> None:
        '''Test the correct stack execution of appened middlewares.
        '''

        class MiddlewareTest(MiddlewareABC):
            async def execute(
                self,
                symbios: Symbios,
                message: Union[IncomingMessage, SendingMessage],
            ) -> None:
                message['test'] += 1

        async def test() -> None:
            midd_lib: MiddlewareLibrary = MiddlewareLibrary()

            message = {'test': 0}

            midd_lib.append(MiddlewareTest(event))
            midd_lib.append(MiddlewareTest(event))
            midd_lib.append(MiddlewareTest(event))
            midd_lib.append(MiddlewareTest(event))

            await midd_lib.run_until_end(None, message, event)

            assert message['test'] == 4

        run_async(test)
