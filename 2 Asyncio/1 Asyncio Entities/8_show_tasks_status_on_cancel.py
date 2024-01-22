import asyncio


async def worker(i: int):
    print(f'worker {i} start')
    try:
        while True:
            print(f'worker {i} new round')
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print(f'worker {i} was cancelled')

    print(f'worker {i} finish')


async def worker_with_exception(i: int):
    await asyncio.sleep(1)
    print(f'worker {i} exception')
    raise Exception


async def main():
    done, pending = await asyncio.wait(
        [*[worker(i) for i in range(1, 4)], worker_with_exception(4)],
        return_when=asyncio.FIRST_EXCEPTION
    )

    print(f'done {len(done)}, pending {len(pending)}')

    for p in pending:
        p.cancel()

    await asyncio.gather(*pending)


if __name__ == '__main__':
    asyncio.run(main())
