import asyncio
import aiohttp


async def post_many_file():
    async with aiohttp.ClienSession() as session:
        data = aiohttp.FormData()
        data.add_field(
            'file1',
            open('README.md', 'rb'),
            filename='READMEmd',
            content_type='text/plain'
        )
        data.add_field(
            'massive-file',
            open('massive-file', 'rb'),
            filename='massive-file',
            content_type='text/plain'
        )
        async with session.post('http://httpbin.org/post', data=data) as r:
            print('Response:', await r.text())

if __name__ == '__main__':
    asyncio.run(post_many_file())
