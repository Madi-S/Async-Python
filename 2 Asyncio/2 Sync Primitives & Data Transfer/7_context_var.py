import asyncio
from contextvars import ContextVar


global_var:	ContextVar[int] = ContextVar('global_var', default=None)


async def printer(i: int):
    print(f'printer	{i}	global_var={global_var.get()}')
    global_var.set(i)
    print(f'printer	{i}	global_var={global_var.get()}')


async def main():
    await asyncio.gather(*[printer(i + 1) for i in range(3)])

if __name__ == '__main__':
    asyncio.run(main())

# >>> printer 1 global_var=None
# >>> printer 1 global_var=1
# >>> printer 2 global_var=None
# >>> printer 2 global_var=2
# >>> printer 3 global_var=None
# >>> printer 3 global_var=3
