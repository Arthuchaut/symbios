from typing import Callable, List, Tuple

import pytest

from symbios import Symbios
from symbios.utils import Props, ArgumentsType
from symbios.queue import Queue
from symbios.consumer import Consumer
from symbios.confirmation import ListenACK


class TestConsumer:
    '''The Consumer class tests.
    '''

    LISTEN_DATASET: List[Tuple[Queue, bool, bool, ArgumentsType, str]] = [
        (Queue('symbios_tests'), False, False, None, None),
        (Queue('symbios_tests'), True, False, None, None),
    ]

    @pytest.mark.parametrize(
        'queue, no_ack, exclusive, arguments, consumer_tag', LISTEN_DATASET
    )
    def test_listen(
        self,
        symbios: Symbios,
        listener_handler: Callable,
        run_async: Callable,
        queue: Queue,
        no_ack: bool,
        exclusive: bool,
        arguments: ArgumentsType,
        consumer_tag: str,
    ) -> None:
        '''Test the consumer listener.
        '''

        async def test() -> None:
            consumer: Consumer = Consumer(
                symbios=symbios,
                queue=queue,
                no_ack=no_ack,
                exclusive=exclusive,
                arguments=arguments,
                consumer_tag=consumer_tag,
                midd_library=symbios._midd_library,
            )

            ack: ListenACK = await consumer.listen(listener_handler)

            assert isinstance(ack, ListenACK)

        run_async(test)
