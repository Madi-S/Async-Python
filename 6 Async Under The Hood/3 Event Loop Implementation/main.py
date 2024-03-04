from dataclasses import dataclass, field
import socket
from selectors import EVENT_READ, EVENT_WRITE, BaseSelector, DefaultSelector
import time
from yarl import URL


class Future:
    def __init__(self):
        self._result = None
        self._is_done = False
        self._callbacks = []

    @property
    def result(self):
        return self._result

    @property
    def is_done(self):
        return self._is_done

    def set_result(self, value):
        self._result = value
        self._is_done = True
        for callback in self._callbacks:
            callback(self)

    def add_done_callback(self, callback):
        self._callbacks.append(callback)

    def __iter__(self):
        yield self
        return self.result


class Task(Future):
    def __init__(self, coro):
        super().__init__()
        self._coro = coro

        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future: Future):
        try:
            f = self._coro.send(future.result)
        except StopIteration as e:
            self.set_result(e.value)
            return
        f.add_done_callback(self.step)


class AsyncSocket:
    def __init__(self):
        self._sock = socket.socket()
        self._sock.setblocking(False)

    def connect(self, host: str, port: int):
        try:
            self._sock.connect((host, port))
        except OSError:
            pass

        f = Future()

        def callback():
            get_event_loop().selector.unregister(self._sock.fileno())
            f.set_result(None)

        get_event_loop().selector.register(self._sock.fileno(), EVENT_WRITE, callback)

        return (yield from f)

    def send(self, data: bytes):
        f = Future()

        def callback():
            get_event_loop().selector.unregister(self._sock.fileno())
            result = self._sock.send(data)
            f.set_result(result)

        get_event_loop().selector.register(self._sock.fileno(), EVENT_WRITE, callback)

        return (yield from f)

    def read(self, size: int = 4096):
        f = Future()

        def callback():
            get_event_loop().selector.unregister(self._sock.fileno())
            result = self._sock.recv(size)
            f.set_result(result)

        get_event_loop().selector.register(self._sock.fileno(), EVENT_READ, callback)

        return (yield from f)

    def read_all(self):
        buffer = bytearray()
        chunk = yield from self.read()
        while chunk:
            buffer.extend(chunk)
            chunk = yield from self.read()
        return bytes(buffer)


@dataclass(order=True)
class TimeFuture:
    dt: float
    future: Future = field(compare=False)


class EventLoop:
    def __init__(self):
        self._selector = DefaultSelector()
        self._tasks: set[Task] = set()
        self._current_time = time.time()
        self._timer: list[TimeFuture] = []

    @property
    def selector(self) -> BaseSelector:
        return self._selector

    def create_task(self, task: Task):
        self._tasks.add(task)

    def call_later(self, timeout: float, future: Future):
        tf = TimeFuture(self._current_time + timeout, future)
        self._timer.append(tf)
        self._timer.sort()

    def run(self):
        while self._tasks:
            self._current_time = time.time()

            while self._timer and self._timer[0].dt <= self._current_time:
                tf = self._timer.pop(0)
                tf.future.set_result(None)

            if self._selector.get_map():
                events = self._selector.select()
                for event_key, _ in events:
                    event_key.data()
            else:
                if self._timer:
                    dt = self._timer[0].dt - time.time()
                    time.sleep(dt)

            for task in self._tasks.copy():
                if task.is_done:
                    self._tasks.remove(task)

        self.selector.close()


_GlobalEventLoop = EventLoop()


def get_event_loop() -> EventLoop:
    global _GlobalEventLoop
    return _GlobalEventLoop


class HttpClient:
    def __init__(self):
        pass

    def get(
        self,
        url: str,
        query: dict[str, str] | None = {},
        headers: dict[str, str] | None = {}
    ):
        u = URL(url)
        u = u.with_query(query)

        headers['Host'] = u.host
        headers['Connection'] = 'close'
        headers_str = '\r\n'.join(
            f'{key}: {value}'
            for key, value in headers.items()
        )

        request = f'GET {u.path_qs} HTTP/1.1\r\n{headers_str}\r\n\r\n'

        s = AsyncSocket()
        yield from s.connect(u.host, u.port)
        yield from s.send(request.encode())
        return (yield from s.read_all())


def gather(*coros: callable):
    results = {}
    gather_future = Future()

    def on_task_done(f):
        results[f] = f.result

        if len(results) == len(coros):
            gather_future.set_result(results)

    tasks = []
    for coro in coros:
        task = Task(coro)
        task.add_done_callback(on_task_done)
        tasks.append(task)
        get_event_loop().create_task(task)

    yield from gather_future

    return [results[task] for task in tasks]


def sleep(timeout: float):
    f = Future()
    get_event_loop().call_later(timeout, f)
    yield from f


def main():
    client = HttpClient()

    yield from gather(
        sleep(1.0),
        sleep(1.0),
        client.get('http://python.org/', query={'foo': 'bar'}),
        client.get('http://python.org/', query={'foo': 'bar'}),
        client.get('http://python.org/', query={'foo': 'bar'}),
        sleep(1.0),
        gather(
            client.get('http://python.org/', query={'foo': 'bar'}),
            client.get('http://python.org/', query={'foo': 'bar'}),
            client.get('http://python.org/', query={'foo': 'bar'}),
            sleep(1.0),
        )
    )
    # Total time: 1.0 seconds


if __name__ == '__main__':
    start_time = time.monotonic()

    loop = get_event_loop()
    loop.create_task(Task(main()))
    loop.run()

    finish_time = time.monotonic()
    print(f'Total time: {finish_time - start_time} seconds')
