import asyncio
import os
from aio_pika import connect, IncomingMessage, ExchangeType


async def create_connection():
    return await connect(url=os.getenv('RABBITMQ_URL'))


async def on_message(message: IncomingMessage):
    async with message.process():
        with open('logs.txt', 'a') as f:
            f.write(str(message))
            f.write('\n')


async def receiver():
    connection = await create_connection()
    channel = await connection.channel()
    logs_exchange = await channel.declare_exchange(
        'logs_level', ExchangeType.DIRECT
    )
    queue = await channel.declare_queue(exclusive=True)
    await queue.bind(logs_exchange, routing_key='critical')
    await queue.consume(on_message)


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(receiver())
    print('[*] Waiting for messages.')
    loop.run_forever()


if __name__ == '__main__':
    main()
