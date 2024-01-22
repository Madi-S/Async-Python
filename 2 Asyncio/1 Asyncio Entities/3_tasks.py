import asyncio


async def worker(idx: int):
    while True:
        print(f'worker-{idx} message')
        await asyncio.sleep(1)


async def main():
    # Create 3 tasks
    for i in range(3):
        asyncio.create_task(worker(i + 1))
    
    while True:
        print(f'main message')
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
