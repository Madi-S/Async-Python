import os
import asyncio
from aio_pika import connect, IncomingMessage, ExchangeType


async def create_connection():
    return await connect(url=os.getenv('RABBITMQ_URL'))


async def on_message(message: IncomingMessage):
    async with message.process():
        with open('logs.txt', 'w') as f:
            f.write(str(message))
            f.write('\n')


async def receiver():
    connection = await create_connection()
    channel = await connection.channel()
    logs_exchange = await channel.declare_exchange(
        'logs', ExchangeType.FANOUT
    )
    queue = await channel.declare_queue('logger')
    await queue.bind(logs_exchange)
    await queue.consume(on_message)


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(receiver())
    print('[*] Waiting for messages.')
    loop.run_forever()


if __name__ == '__main__':
    main()
