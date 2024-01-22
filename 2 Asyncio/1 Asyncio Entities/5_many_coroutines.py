import asyncio
import random


async def random_sleep(i: int):
    delay = random.randint(1, 4)
    print(f'[START {i}] Sleeping for {delay} seconds')
    await asyncio.sleep(delay)
    print(f'[END {i}] Sleeping for {delay} seconds')


async def main():
    await asyncio.gather(random_sleep(1), random_sleep(2), random_sleep(3))


if __name__ == '__main__':
    asyncio.run(main())
