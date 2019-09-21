# Symbios

An asynchronous messaging queue manager based on [aiormq](https://github.com/mosquito/aiormq).

![GitHub top language](https://img.shields.io/github/languages/top/arthuchaut/symbios)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/arthuchaut/symbios)
![GitHub](https://img.shields.io/github/license/arthuchaut/symbios)

## Table of Contents

- [Symbios](#symbios)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Getting Started](#getting-started)
    - [Emit Message](#emit-message)
    - [Listen Message](#listen-message)
    - [RPC Pattern](#rpc-pattern)
      - [Server Side](#server-side)
      - [Client Side](#client-side)
  - [Documentation](#documentation)
    - [Development Guide](#development-guide)
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

## Getting Started

This guide is a quick demonstration of how to use Symbios.

### Emit Message

```python
from symbios import Symbios
from symbios.message import SendingMessage

async def main() -> None:
    broker: Symbios = Symbios(host='broker.domain.name.or.ip.addr.dev')

    message: SendingMessage = SendingMessage('Lapin !')
    await broker.emit(message, routing_key='my_queue')

if __name__ == '__main__':
    loop: EventLoop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### Listen Message

```python
from symbios import Symbios
from symbios.message import IncomingMessage
from symbios.queue import Queue

async def on_receive_handler(broker: Symbios, message: IncomingMessage) -> None:
    print(f'Received message that contains: {message.deserialized}')

async def main() -> None:
    broker: Symbios = Symbios(host='broker.domain.name.or.ip.addr.dev')
    
    queue: Queue = Queue('my_queue')
    await broker.listen(on_receive_handler, queue=queue, no_ack=True)

if __name__ == '__main__':
    loop: EventLoop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### RPC Pattern

The RPC pattern (called *Remote Procedure Call*) is a procedure to send a request to the broker and waiting for its response back.

#### Server Side

```python
from symbios import Symbios, Props
from symbios.message import SendingMessage

async def on_receive_handler(broker: Symbios, message: IncomingMessage) -> None:
    indentity: Dict[str, Union[str, int]] = message.deserialized

    response: str = (f'Hi, {identity["firstname"]} {identity["lastname"]}. '
                     f'You look pretty young for {identity["age"]} years old.')
    
    sen_message: SendingMessage = SendingMessage(response)

    await broker.emit(
        sen_message, 
        routing_key=message.props.reply_to, 
        props=Props(correlation_id=message.props.correlation_id)
    )

async def main() -> None:
    broker: Symbios = Symbios(host='broker.domain.name.or.ip.addr.dev')

    queue: Queue = Queue('my_queue')
    await broker.declare_queue(queue)
    broker.listen(on_receive_handler, queue=queue, no_ack=True)

if __name__ == '__main__':
    loop: EventLoop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

#### Client Side

```python
from symbios import Symbios
from symbios.message import IncomingMessage, SendingMessage

async def main() -> None:
    broker: Symbios = Symbios(host='broker.domain.name.or.ip.addr.dev')

    sen_message: SendingMessage = SendingMessage({
        'firstname ': 'Keanu', 
        'lastname': 'Reeves', 
        'age': 55
    })

    inc_message: IncomingMessage = await broker.rpc.call(sen_message, routing_key='my_queue')
    print(f'Received message that contains: {inc_message.deserialized}')

if __name__ == '__main__':
    loop: EventLoop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Documentation

### Development Guide

...

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