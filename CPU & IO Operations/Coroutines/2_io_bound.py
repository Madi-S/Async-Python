import asyncio
import time


SUB_PROGS_COUNT = 1000


async def worker():
    await asyncio.sleep(1)


async def main():
    begin = time.time()
    await asyncio.gather(
        *[worker() for _ in range(SUB_PROGS_COUNT)]
    )
    print(time.time() - begin)


asyncio.run(main())
# Done in approximately 1 second
# However, 1000 tasks for 1 second were executed
