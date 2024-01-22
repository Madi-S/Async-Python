import asyncio


class PackOfChips:
    def __init__(self):
        self._lock = asyncio.Lock()

    async def reverse(self):
        await self._lock.acquire()

    def cheeps(self):
        self._lock.release()


async def handle(name: str, pack: PackOfChips):
    await pack.reverse()
    print(f'{name} has put hand in pack of chips')
    await asyncio.sleep(1)
    pack.cheeps()
    print(f'{name} has taken chips')


async def main():
    people = ['Jim', 'Alex', 'Ashely', 'Karl']
    pack = PackOfChips()
    await asyncio.gather(*[handle(name, pack) for name in people])


if __name__ == '__main__':
    asyncio.run(main())

# >>> Jim has put hand in pack of chips
# >>> Jim has taken chips
# >>> Alex has put hand in pack of chips
# >>> Alex has taken chips
# >>> Ashely has put hand in pack of chips
# >>> Ashely has taken chips
# >>> Karl has put hand in pack of chips
# >>> Karl has taken chips
