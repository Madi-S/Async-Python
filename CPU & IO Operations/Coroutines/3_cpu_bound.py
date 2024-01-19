import asyncio
import time


SUB_PROGS_COUNT = 1000


async def worker(_id: int):
    i = 0
    begin = time.time()
    while i < 50_000:
        i += 1
    print(f'ID: {_id} FINISH duration: {time.time() - begin}')


async def main():
    begin = time.time()
    await asyncio.gather(
        *[worker(i) for i in range(SUB_PROGS_COUNT)]
    )
    print(f'ALL COROUTINES DONE duration: {time.time() - begin}')


asyncio.run(main())
# No time efficiency here
# Because operations in coroutine `worker` are synchronous
