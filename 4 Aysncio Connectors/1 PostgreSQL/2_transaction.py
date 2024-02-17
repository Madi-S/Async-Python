import os
import typing
import asyncio
import datetime

import asyncpg


async def get_connection_by_dsn():
    '''
    POSTGRES_DSN = postgres://user:password@host:port/database
    '''
    return await asyncpg.connect(os.getenv('POSTGRES_DSN'))


async def insert_many(connection) -> asyncpg.Record:
     async with connection.transaction():
        for i in range(10):
            name = f'name {i}'
            await connection.execute(
                "insert into users (first_name, last_name, is_active, created_at) values ($1, $2, $3, $4)",
                name, name, True, datetime.datetime.now()
            )


async def transaction_with_error(connection) -> None:
    async with connection.transaction():
        await insert_many(connection)
        1 / 0


async def select_many(connection) -> typing.AsyncIterator[asyncpg.Record]:
    async with connection.transaction():
        cursor = await connection.cursor('select * from users')
        chunk = await cursor.fetch(5)
        while chunk:
            for item in chunk:
                yield item
                chunk = await cursor.fetch(5)


async def main() -> None:
    connection = await get_connection_by_dsn()
    
    await insert_many(connection)
    
    try:
        await transaction_with_error(connection)
    except ZeroDivisionError:
        pass
    
    async for record in select_many(connection):
        print('select many record:', record)


if __name__ == '__main__':
    asyncio.run(main())
