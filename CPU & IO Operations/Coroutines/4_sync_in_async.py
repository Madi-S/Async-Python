import asyncio
import time


SUB_PROGS_COUNT = 10


async def sync_sleep():
    time.sleep(1)


async def async_sleep():
    await asyncio.sleep(1)


async def main():
    begin = time.time()
    await asyncio.gather(
        *[async_sleep() for _ in range(SUB_PROGS_COUNT)]
    )
    print(f'asynchronous sleep execution: {time.time() - begin}')

    begin = time.time()
    await asyncio.gather(
        *[sync_sleep() for _ in range(SUB_PROGS_COUNT)]
    )
    print(f'synchronous sleep execution: {time.time() - begin}')


asyncio.run(main())
# asynchronous sleep execution: 1.01643705368042
# synchronous sleep execution: 10.003939628601074
# `time.sleep()` is a blocker function, unlike `asyncio.sleep()`