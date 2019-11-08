# Symbios

![](https://github.com/Arthuchaut/storage/raw/master/symbios/symbios_github_banner_left.png)

An asynchronous messaging queue manager based on [aiormq](https://github.com/mosquito/aiormq).

![GitHub top language](https://img.shields.io/github/languages/top/arthuchaut/symbios)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/arthuchaut/symbios)
![GitHub](https://img.shields.io/github/license/arthuchaut/symbios)

## Table of Contents

- [Symbios](#symbios)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Getting Started](#getting-started)
    - [Instalation](#instalation)
    - [Emit Message](#emit-message)
    - [Listen Message](#listen-message)
    - [RPC Pattern](#rpc-pattern)
      - [Server Side](#server-side)
      - [Client Side](#client-side)
  - [Documentation](#documentation)
    - [Development Guide](#development-guide)
      - [Installation](#installation)
    - [Deployment Guide](#deployment-guide)
    - [Symbios Engine](#symbios-engine)
      - [Emitter](#emitter)
      - [Listener](#listener)
      - [RPC](#rpc)
      - [Middleware](#middleware)
      - [Message](#message)
      - [Queue](#queue)
      - [Exchange](#exchange)
    - [Code of Development](#code-of-development)
  - [License](#license)

## Introduction

Symbios is a Python library for communicating with **AMQP** brokers, like **RabbitMQ**.  
Its engine is based on the [aiormq](https://github.com/mosquito/aiormq) library allowing an asynchronous management of communications.  
Observing the communication mechanism of the AMPQ protocol, I wanted to implement a model similar to that of websockets for a simplified use.  
Note that this vision needs medium-term tests before it can perhaps be validated later.

## Requirements

- Python >= 3.7.*

## Getting Started

This guide is a quick demonstration of Symbios basics.  

### Instalation

**Note:** This library aims to be available on the **Pypi** packagist from its beta release.  
In the meantime, you must retrieve this repository to use it.  
Also note that the code examples below are written in the context of an import of **Pypi**.  
You will therefore have to readjust the imports.

To import the project, see the [Installation](#installation) guide.

### Emit Message

```python
import asyncio
from symbios import Symbios
from symbios.message import SendingMessage

async def main() -> None:
    broker: Symbios = Symbios(
        host='broker.host',
        user='username', 
        password='password'
    )

    await broker.emit(SendingMessage('Lapin !'), routing_key='my_queue')

if __name__ == '__main__':
    asyncio.run(main())
```

### Listen Message

```python
import asyncio
from symbios import Symbios
from symbios.message import IncomingMessage
from symbios.queue import Queue

async def on_receive_handler(broker: Symbios, message: IncomingMessage) -> None:
    print(f'Received message that contains: {message.deserialized}')

async def main() -> None:
    broker: Symbios = Symbios(
        host='broker.host',
        user='username', 
        password='password'
    )
    
    await broker.listen(on_receive_handler, queue=Queue('my_queue'), no_ack=True)

if __name__ == '__main__':
    asyncio.run(main())
```

### RPC Pattern

The RPC pattern (called *Remote Procedure Call*) is a procedure to send a request to the broker and waiting for its response back.

#### Server Side

```python
from symbios import Symbios
from symbios.utils import Props
from symbios.message import SendingMessage

async def on_receive_handler(broker: Symbios, message: IncomingMessage) -> None:
    tram: Dict[str, Union[str, int]] = message.deserialized

    if tram['message'] is 'SYN':
        await broker.emit(
            SendingMessage({'message': 'SYN-ACK'}),
            routing_key=message.props.reply_to,
            props=Props(correlation_id=message.props.correlation_id),
        )

async def main() -> None:
    broker: Symbios = Symbios(
        host='broker.host',
        user='username', 
        password='password'
    )

    await broker.listen(on_receive_handler, queue=Queue('rpc_queue'), no_ack=True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
```

#### Client Side

```python
import asyncio
from symbios import Symbios
from symbios.message import IncomingMessage, SendingMessage

async def main() -> None:
    # Create a connection to the broker
    broker: Symbios = Symbios(
        host='broker.host',
        user='username', 
        password='password'
    )

    # Await for the server response back
    res: IncomingMessage = await broker.rpc.call(
        SendingMessage({'message': 'SYN'}), # Create a message that contains a Dict
        routing_key='rpc_queue' # Specify the routing_key to send the call
    )

    print(f'Received message that contains: {res.deserialized}')
    # Should print "Received message that contains: {'message': 'SYN-ACK'}"

if __name__ == '__main__':
    asyncio.run(main())
```

## Documentation

### Development Guide

#### Installation

You must first clone the repository.  
Then go to the root of the project, then install the dependencies via **Pipenv**.

    pipenv install --dev --pre

The project is now ready for development !

### Deployment Guide

...

### Symbios Engine

#### Emitter

...

#### Listener

...

#### RPC

...

#### Middleware

...

#### Message

...

#### Queue

...

#### Exchange

...

### Code of Development

...

## License

Licensed under the [MIT](LICENSE) license.