from typing import Any
import asyncio
from asyncio import Task
from os import environ
from collections import namedtuple

import pytest

from symbios.utils import Props
from symbios import Symbios
from symbios.connector import Connector
from symbios.message import IncomingMessage, SendingMessage
from symbios.queue import Queue
from .mocks import MockSymbios, MockChannel


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
def mocked_channel(monkeypatch) -> None:
    def inner(channel) -> None:
        async def mock_channel_queue_declare(**kwargs):
            return await MockChannel().queue_declare(**kwargs)

        async def mock_channel_basic_publish(*args, **kwargs):
            return await MockChannel().basic_publish(*args, **kwargs)

        monkeypatch.setattr(
            channel, 'queue_declare', mock_channel_queue_declare
        )
        monkeypatch.setattr(
            channel, 'basic_publish', mock_channel_basic_publish
        )

    return inner


@pytest.fixture
def mocked_symbios(symbios, monkeypatch) -> None:
    async def mock_symbios_emit(*args, **kwargs):
        return await MockSymbios(symbios).emit(*args, **kwargs)

    async def mock_symbios_listen(*args, **kwargs):
        return await MockSymbios(symbios).listen(*args, **kwargs)

    async def mock_symbios_declare_queue(*args, **kwargs):
        return await MockSymbios(symbios).declare_queue(*args, **kwargs)

    monkeypatch.setattr(symbios, 'emit', mock_symbios_emit)
    monkeypatch.setattr(symbios, 'listen', mock_symbios_listen)
    monkeypatch.setattr(symbios, 'declare_queue', mock_symbios_declare_queue)

    return symbios


@pytest.fixture
def init_rpc_server(mocked_symbios) -> None:
    async def inner(mocked_symbios) -> None:
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
