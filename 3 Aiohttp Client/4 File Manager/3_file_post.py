import asyncio
import aiohttp


async def post_file():
    async with aiohttp.ClienSession() as session:
        files = {'file': open('massive-file', 'rb')}
        async with session.post('http://httpbin.org/post', data=files) as r:
            print('Response:', await r.text())


if __name__ == '__main__':
    asyncio.run(post_file())
