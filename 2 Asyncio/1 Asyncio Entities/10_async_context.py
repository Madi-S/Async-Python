import asyncio
import time
import typing


async def action():
    print(f'{time.time()}: start sleep')
    await asyncio.sleep(1)
    print(f'{time.time()}: end sleep')


class AsyncContextManager:
    async def __aenter__(self):
        print(f'{time.time()}: __aenter__')
        await asyncio.sleep(1)

    async def __aexit__(self, *_):
        print(f'{time.time()}: __aexit__')
        await action()


async def main():
    async with AsyncContextManager() as acm:
        pass

    await asyncio.sleep(3)


if __name__ == '__main__':
    asyncio.run(main())
