import os
import asyncio

import asyncpg


async def get_connection_by_dsn():
    '''
    POSTGRES_DSN = postgres://user:password@host:port/database
    '''
    return await asyncpg.connect(os.getenv('POSTGRES_DSN'))


async def query(connection):
    print(await connection.fetch('select * from users'))


async def incorrect_approach():
    connection = await get_connection_by_dsn()
    await asyncio.gather(query(connection), query(connection))


if __name__ == '__main__':
    asyncio.run(incorrect_approach())
