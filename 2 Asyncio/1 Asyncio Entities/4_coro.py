import asyncio


async def coro():
    await asyncio.sleep(5)


async def main():
    await coro()

    task = asyncio.create_task(coro())

    await task


if __name__ == '__main__':
    asyncio.run(main())
