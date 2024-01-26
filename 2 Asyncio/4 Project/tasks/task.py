import asyncio
from dataclasses import dataclass


@dataclass
class Task:
    async def perform(self, pool):
        pass

# @dataclass
# class Task:
#     tid: int

#     async def perform(self, pool):
#         print('start perform', self.tid)
#         await asyncio.sleep(3)
#         print('complete perform', self.tid)
