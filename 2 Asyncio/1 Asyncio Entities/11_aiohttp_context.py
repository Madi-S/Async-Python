import asyncio
import aiohttp
from aioresponses import aioresponses


url = 'http://service.ru'
payload = dict(crowd=['Andrey', 'Alex', 'Artem', 'Igor'])


async def main():
    with aioresponses() as m:
        m.get(url, payload=payload)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                json = await response.json()
    print(json)


data = asyncio.run(main())
