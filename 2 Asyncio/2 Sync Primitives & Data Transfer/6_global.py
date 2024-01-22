import asyncio


global_var = None


async def printer(i: int):
    global global_var
    print(f'printer {i} global_var={global_var}')
    global_var = i
    print(f'printer {i} global_var={global_var}')


async def main():
    coros = [printer(i + 1) for i in range(3)]
    await asyncio.gather(*coros)


if __name__ == '__main__':
    asyncio.run(main())

# >>> printer 1 global_var=None
# >>> printer 1 global_var=1
# >>> printer 2 global_var=1
# >>> printer 2 global_var=2
# >>> printer 3 global_var=2
# >>> printer 3 global_var=3
