import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('http://example.org/ws') as ws:
            async for ms in ws:
                print('new message', ws)
                

if __name__ == '__main__':
    asyncio.run(main())
    