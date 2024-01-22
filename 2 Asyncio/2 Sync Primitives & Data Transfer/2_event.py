import asyncio


async def wait_and_set(event: asyncio.Event):
    await asyncio.sleep(1)
    event.set()


async def run():
    event = asyncio.Event()
    asyncio.create_task(wait_and_set(event))
    await event.wait()


if __name__ == '__main__':
    asyncio.run(run())
    print('Finish')
