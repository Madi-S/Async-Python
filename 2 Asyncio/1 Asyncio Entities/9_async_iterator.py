import asyncio
import random


class Crowd:
    def __init__(self, people: list[str]):
        self._people = people
        self._i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._i >= len(self._people):
            raise StopAsyncIteration

        person = self._people[self._i]
        self._i += 1
        delay = random.randint(1, 4)
        
        # let us imagine this is a request
        await asyncio.sleep(delay)

        return person


async def main():
    crowd = Crowd(['Alex', 'Tim', 'John', 'Matthew'])
    async for i in crowd:
        print(i)


if __name__ == '__main__':
    asyncio.run(main())
