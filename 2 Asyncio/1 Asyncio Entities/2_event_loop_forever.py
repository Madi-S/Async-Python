import time
import asyncio


async def send_statistic():
    print(f'{time.time()}:	stat')


async def worker():
    while True:
        await asyncio.sleep(60)
        await send_statistic()


# get event loop
loop = asyncio.get_event_loop()
# add task to event loop
loop.create_task(worker())
# run tasks in event loop forever
loop.run_forever()
