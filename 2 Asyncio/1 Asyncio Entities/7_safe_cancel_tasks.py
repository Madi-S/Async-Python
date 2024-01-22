import asyncio


async def db_operation():
    print('operation start')
    try:
        while True:
            print('operation new round')
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print('operation was cancelled')
        await asyncio.sleep(1)

    print('operation finish')


async def main():
    task = asyncio.create_task(db_operation())
    await asyncio.sleep(2.1)

    task.cancel()
    await task


if __name__ == '__main__':
    asyncio.run(main())

# >>> operation start
# >>> operation new round
# >>> operation new round
# >>> operation new round
# >>> operation was cancelled
# >>> operation finish
