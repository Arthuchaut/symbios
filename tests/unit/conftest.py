from typing import Any
import asyncio
from asyncio import Task
from os import environ
from collections import namedtuple

import pytest

from libs.symbios import Symbios, Props
from libs.symbios.connector import Connector
from libs.symbios.message import IncomingMessage, SendingMessage
from libs.symbios.queue import Queue
from .mocks import MockSymbios


@pytest.fixture
def symbios() -> Symbios:
    return Symbios(
        host=environ['SYMBIOS_HOST'] or None,
        port=environ['SYMBIOS_PORT'] or None,
        vhost=environ['SYMBIOS_VHOST'] or None,
        user=environ['SYMBIOS_USER'] or None,
        password=environ['SYMBIOS_PASSWORD'] or None,
    )


@pytest.fixture
def connector() -> Connector:
    return Connector(
        host=environ['SYMBIOS_HOST'] or None,
        port=environ['SYMBIOS_PORT'] or None,
        vhost=environ['SYMBIOS_VHOST'] or None,
        user=environ['SYMBIOS_USER'] or None,
        password=environ['SYMBIOS_PASSWORD'] or None,
    )


@pytest.fixture
def run_async() -> None:
    def run(task: Task) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(task())

    return run


@pytest.fixture
def delivered_message_model() -> None:
    def inner(delivery, header, body) -> None:
        HeaderModel = namedtuple('HeaderModel', 'properties')
        DeliveredMessageModel = namedtuple(
            'DeliveredMessageModel', 'delivery, header, body'
        )

        return DeliveredMessageModel(delivery, HeaderModel(header), body)

    return inner


@pytest.fixture
def mocked_symbios(symbios, monkeypatch) -> None:
    async def mock_symbios_emit(*args, **kwargs):
        return await MockSymbios(symbios).emit(*args, **kwargs)

    async def mock_symbios_listen(*args, **kwargs):
        return await MockSymbios(symbios).listen(*args, **kwargs)

    monkeypatch.setattr(symbios, 'emit', mock_symbios_emit)
    monkeypatch.setattr(symbios, 'listen', mock_symbios_listen)

    return symbios


@pytest.fixture
def init_rpc_server(mocked_symbios) -> None:
    async def inner() -> None:
        async def listen_handler(symbios_sck, message):
            await symbios_sck.emit(
                SendingMessage('RPC_ACK'),
                routing_key=message.props.reply_to,
                props=Props(correlation_id=message.props.correlation_id),
            )

        await mocked_symbios.listen(
            listen_handler, queue=Queue('symbios_tests')
        )

    return inner


@pytest.fixture
def listener_handler() -> None:
    async def handler(symbios: Symbios, message: IncomingMessage) -> None:
        ...

    return handler
