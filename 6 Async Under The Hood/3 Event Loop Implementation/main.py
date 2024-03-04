import socket
from selectors import EVENT_READ, EVENT_WRITE, BaseSelector, DefaultSelector
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


class EventLoop:
    def __init__(self):
        self._selector = DefaultSelector()
        self._tasks: set[Task] = set()

    @property
    def selector(self) -> BaseSelector:
        return self._selector

    def create_task(self, task: Task):
        self._tasks.add(task)

    def run(self):
        while self._tasks:
            events = self._selector.select()
            for event_key, _ in events:
                event_key.data()

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
        response = yield from s.read_all()
        return response


def main():
    client = HttpClient()
    result = yield from client.get('http://python.org/')
    print(result.decode())


if __name__ == '__main__':
    loop = get_event_loop()
    loop.create_task(Task(main()))
    loop.run()
