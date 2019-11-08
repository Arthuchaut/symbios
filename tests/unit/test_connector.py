from typing import Callable
from asyncio import AbstractEventLoop

import pytest

from symbios import Symbios
from symbios.utils import Connection, Channel
from symbios.connector import Connector, ConnectorError


class TestConnector:
    '''The Connector unit tests.
    '''

    def test_connection(
        self, connector: Connector, run_async: Callable
    ) -> None:
        '''Test the Connector connection.
        '''

        async def test() -> None:
            conn: Connector = await connector.connection

            assert type(conn) == Connection

            other_connector: Connector = Connector(host='')

            with pytest.raises(ConnectorError):
                await other_connector.connection

        run_async(test)

    def test_channel(self, connector: Connector, run_async: Callable) -> None:
        '''Test the Connector channel
        '''

        async def test():
            chan: Channel = await connector.channel

            assert type(chan) == Channel

            other_connector: Connector = Connector(host='')

            with pytest.raises(ConnectorError):
                await other_connector.channel

        run_async(test)

    def test_event_loop(self, connector: Connector) -> None:
        '''The the Connector event loop retriever.
        '''

        loop: AbstractEventLoop = connector.event_loop

        assert isinstance(loop, AbstractEventLoop)

    def test_url(self, connector: Connector) -> None:
        '''Test the Connector._url attribute.
        '''

        expected_url: str = (
            f'{connector._protocol}://{connector._user}:{connector._password}'
            f'@{connector._host}{connector._vhost}'
        )

        assert connector._url == expected_url

