'''
@desc    The broker connector class.
@author  arthuchaut <arthuchaut@gmail.com>
@version 0.1.0
@date    2019-09-20
@note    0.1.0 (2019-09-20): Writed the first drafts.
'''

import asyncio
from asyncio.events import AbstractEventLoop

import aiormq
from aiormq import Connection, Channel
from aiormq.exceptions import ProbableAuthenticationError


class Connector:
    '''Class allowing to create a connection to the broker.

    Attributes:
        _DEFAULT_PROTOCOL (str): The broker communication protocol.
        _DEFAULT_HOST (str): The broker hostname or ip address.
        _DEFAULT_VHOST (str): The connection virtual host.
        _DEFAULT_PORT (int): The broker listening port.
        _DEFAULT_USER (str): The username to connect.
        _DEFAULT_PASSWORD (str): The password to connect.

        _protocol (str): The broker communication protocol. 
        _host (str): The broker hostname or ip address.
        _vhost (str): The connection virtual host.
        _port (int): The broker listening port.
        _user (str): The username to connect.
        _password (str): The password to connect.
        _connection (Connection): The broker established connection.
        event_loop (AbstractEventLoop): The asyncio event loop.
            Try to get the running event loop, else create a new instance.
        _url (str): The built url for establishing the broker connection.
        connection (Connection): The broker established connection.
            Create a connection if isn't exists.
        channel (Channel): The connection channel.
    '''

    _DEFAULT_PROTOCOL: str = 'amqp'
    _DEFAULT_HOST: str = 'localhost'
    _DEFAULT_VHOST: str = '/'
    _DEFAULT_PORT: int = 5672
    _DEFAULT_USER: str = 'guest'
    _DEFAULT_PASSWORD: str = 'guest'

    def __init__(
        self,
        *,
        protocol: str = _DEFAULT_PROTOCOL,
        host: str = _DEFAULT_HOST,
        vhost: str = _DEFAULT_VHOST,
        port: int = _DEFAULT_PORT,
        user: str = _DEFAULT_USER,
        password: str = _DEFAULT_PASSWORD,
    ):
        '''The Connector initializer.

        Args:
            _protocol (str): The broker communication protocol. 
                Default to _DEFAULT_PROTOCOL.
            _host (str): The broker hostname or ip address.
                Default to _DEFAULT_HOST.
            _vhost (str): The connection virtual host.
                Default to _DEFAULT_VHOST.
            _port (int): The broker listening port.
                Default to _DEFAULT_PORT.
            _user (str): The username to connect.
                Default to _DEFAULT_USER.
            _password (str): The password to connect.
                Default to _DEFAULT_PASSWORD.
            _connection (Connection): The broker established connection.
            _url (str): The built url for establishing the broker connection.
            connection (Connection): The broker established connection.
                Create a connection if isn't exists.
            channel (Channel): The connection channel.
        '''

        self._protocol: str = protocol
        self._host: str = host
        self._vhost: str = Connector._DEFAULT_VHOST + vhost
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._connection: Connection = None

    @property
    def event_loop(self) -> AbstractEventLoop:
        '''Try to retrieve the current event loop if exists.
        
        Retreive the running event loop. If it doesn't exists yet,
        then create a new event loop.

        Returns:
            AbstractEventLoop: The asyncio event loop.
        '''

        loop: AbstractEventLoop = None

        try:
            loop = asyncio.get_running_loop()
        except Exception as e:
            loop = asyncio.get_event_loop()

        return loop

    @property
    def _url(self) -> str:
        '''The url builder property.
        Formate an url for establishing the broker connection.

        Returns:
            str: The built url.
        '''

        return (
            f'{self._protocol}://{self._user}:{self._password}'
            f'@{self._host}{self._vhost}'
        )

    @property
    async def connection(self) -> Connection:
        '''The broker connection.
        Create a connection if it isn't created yet.

        Raises:
            ConnectorError: If the connection couldn't be established.

        Returns:
            Connection: The broker connection.
        '''

        if self._connection is None:
            try:
                self._connection = await aiormq.connect(
                    self._url, loop=self.event_loop
                )
            except Exception as e:
                raise ConnectorError(e)

        return self._connection

    @property
    async def channel(self) -> Channel:
        '''The connection channel.

        Returns:
            Channel: The connection channel.
        '''

        return await (await self.connection).channel()


class ConnectorError(Exception):
    '''The ConnectorError exception class.
    '''
