import asyncio
import datetime


async def do_something():
    await asyncio.sleep(5)


class Scheduler:
    def __init__(self, timer: int):
        self.timer = timer
        self.is_running = True
        self._stop_event = asyncio.Event()
        self._scheduler_task: asyncio.Task | None = None
        self._concurrent_workers = 0

    async def _worker(self):
        self._concurrent_workers += 1

        print('start', datetime.datetime.now())
        await do_something()
        print('stop', datetime.datetime.now())

        self._concurrent_workers -= 1
        if not self.is_running and self._concurrent_workers == 0:
            self._stop_event.set()

    async def _scheduler(self):
        while self.is_running:
            asyncio.create_task(self._worker())
            await asyncio.sleep(self.timer)

    def start(self):
        self.is_running = True
        self._scheduler_task = asyncio.get_event_loop(). \
            create_task(self._scheduler())

    async def stop(self):
        self.is_running = False
        self._scheduler_task.cancel()
        await self._stop_event.wait()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    s = Scheduler(2)
    s.start()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(s.stop())
