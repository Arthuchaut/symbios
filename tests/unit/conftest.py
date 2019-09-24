import asyncio
from asyncio import Task
from os import environ

import pytest

from libs.symbios import Symbios
from libs.symbios.connector import Connector
from libs.symbios.message import IncomingMessage


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
def listener_handler() -> None:
    async def handler(symbios: Symbios, message: IncomingMessage) -> None:
        # print(f'message catched: {message.deserialized}')
        ...

    return handler
