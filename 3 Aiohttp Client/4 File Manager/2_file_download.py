import asyncio
import aiohttp


async def download_file(url, destination_path):
    async with aiohttp.ClienSession() as session:
        async with session.get(url) as r:
            with open(destination_path, 'wb') as f:
                async for data in r.content.iter_chunked(1024):
                    f.write(data)


if __name__ == '__main__':
    asyncio.run(download_file('some url', 'my-file.png'))
