import time
import asyncio


class Query:
    async def execute(self):
        await asyncio.sleep(1)


class PGStore:
    def __init__(self):
        # limited concurrent access to the resources
        self._sem = asyncio.Semaphore(2)
        self._init_time = time.time()

    async def execute_request(self, query):
        # every use of this context manager will reduce
        # semaphore counter and once counter = 0
        # coroutines that were not executed will be blocked

        async with self._sem:
            print(f'{time.time() - self._init_time}s request was started')
            await query.execute()
            print(f'{time.time() - self._init_time}s request was handled')


async def main():
    store = PGStore()
    coros = [store.execute_request(Query()) for _ in range(100)]

    await asyncio.gather(*coros)


if __name__ == '__main__':
    asyncio.run(main())
