import os
import asyncio

import asyncpg


async def get_pool_by_dsn():
    return await asyncpg.create_pool(os.getenv('POSTGRES_DSN'))


async def query(connection):
    print(await connection.fetch('select * from users'))


async def pool_query(pool):
    async with pool.acquire() as connection:
        await query(connection)


async def correct_approach():
    pool = await get_pool_by_dsn()
    await asyncio.gather(pool_query(pool), pool_query(pool))


if __name__ == '__main__':
    asyncio.run(correct_approach())
