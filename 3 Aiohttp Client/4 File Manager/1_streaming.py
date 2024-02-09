import asyncio
import aiohttp
import aiofiles


async def first_approach():
    async with aiohttp.ClientSession() as session:
        with open('massive-file', 'rb') as f:
            async with session.post('http://httpbin.org/post', data=f) as r:
                print('Response:', await r.text())


async def second_approach():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://httpbin.org/post',
            data=file_sender('massive-file')
        ) as r:
            print('Response:', await r.text())


async def file_sender(file_name=None):
    async with aiofiles.open(file_name) as f:
        chunk = await f.read(64 * 1024)
        while chunk:
            yield chunk
            chunk = await f.read(64 * 1024)
