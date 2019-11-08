from typing import Callable, List, Tuple

import pytest

from symbios import Symbios
from symbios.utils import Props
from symbios.exchange import Exchange
from symbios.producer import Producer
from symbios.message import SendingMessage
from symbios.confirmation import EmitACK


class TestProducer:
    '''The Producer class tests.
    '''

    CONTENT_TYPE_DATASET: List[Tuple[SendingMessage, str]] = [
        (SendingMessage(''), 'text/plain'),
        (SendingMessage(3.14), 'text/plain'),
        (SendingMessage(42), 'text/plain'),
        (SendingMessage({}), 'application/json'),
    ]

    EMIT_DATASET: List[Tuple[Exchange, str, Props, bool, bool]] = [
        (
            Exchange('symbios_test_direct', exchange_type=Exchange.DIRECT),
            'symbios_test',
            Props(),
            False,
            False,
        ),
        (
            Exchange('symbios_test_fanout', exchange_type=Exchange.FANOUT),
            'symbios_test',
            Props(),
            False,
            False,
        ),
        (
            Exchange('symbios_test_topic', exchange_type=Exchange.TOPIC),
            'symbios_test',
            Props(),
            False,
            False,
        ),
        (
            Exchange('symbios_test_headers', exchange_type=Exchange.HEADERS),
            'symbios_test',
            Props(),
            False,
            False,
        ),
    ]

    @pytest.mark.parametrize(
        'exchange, routing_key, props, mandatory, immediate', EMIT_DATASET
    )
    def test_emit(
        self,
        symbios: Symbios,
        mocked_channel,
        run_async: Callable,
        exchange: Exchange,
        routing_key: str,
        props: Props,
        mandatory: bool,
        immediate: bool,
    ) -> None:
        '''Test the producer emitter.
        '''

        async def test() -> None:
            producer: Producer = Producer(
                symbios=symbios,
                exchange=exchange,
                routing_key=routing_key,
                props=props,
                mandatory=mandatory,
                immediate=immediate,
                midd_library=symbios._midd_library,
            )

            mocked_channel(await producer.symbios.channel)

            message: SendingMessage = SendingMessage('lapin')

            ack: EmitACK = await producer.emit(message)

            assert isinstance(ack, EmitACK)

        run_async(test)

    @pytest.mark.parametrize('message, content_type', CONTENT_TYPE_DATASET)
    def test__determine_content_type(
        self, symbios: Symbios, message: SendingMessage, content_type: str
    ) -> None:
        '''Test the producer content_type determiner.
        '''

        producer: Producer = Producer(
            symbios=symbios, midd_library=symbios._midd_library
        )

        assert producer._determine_content_type(message) == content_type
