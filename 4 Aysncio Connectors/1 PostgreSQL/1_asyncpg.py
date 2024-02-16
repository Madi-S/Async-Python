import os
import asyncio
import datetime

import asyncpg


async def get_connection():
    return await asyncpg.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database=os.getenv('POSTGRES_DATABASE')
    )


async def get_connection_by_dsn():
    '''
    POSTGRES_DSN = postgres://user:password@host:port/database
    '''
    return await asyncpg.connect(os.getenv('POSTGRES_DSN'),)


async def insert(connection) -> asyncpg.Record:
    res = await connection.fetchrow(
        'insert into users (first_name, last_name, is_active, created_at) values ($1, $2, $3, $4) returning *',
        'Dominic', 'Thiem', True, datetime.datetime.now()
    )
    return res


async def select(connection, user_id) -> list[asyncpg.Record]:
    res = await connection.fetch('select * from users where id = $1', user_id)
    return res


async def update(connection, user_id) -> asyncpg.Record | None:
    return await connection.fetchrow('update users set is_active = false where id = $1 returning *', user_id)


async def delete(connection, user_id) -> None:
    res = await connection.execute('delete from users where id = $1', user_id)
    print(type(res), res)


async def run():
    connection = await get_connection_by_dsn()

    res = await insert(connection)
    print('Insert', res)

    user_id = res['id']
    res = await select(connection, user_id)
    print('Select', res)

    res = await update(connection, user_id)
    print('Update', res)

    await delete(connection, user_id)
    res = await select(connection, user_id)
    print('After Delete', res)
