import socket
from selectors import EVENT_READ, EVENT_WRITE, BaseSelector, DefaultSelector


class Future:
    def __init__(self):
        self._result = None
        self._is_done = False
        self._callbacks = []

    @property
    def result(self):
        return self._result

    def set_result(self, value):
        self._result = value
        self._is_done = True
        for callback in self._callbacks:
            callback(self)

    def add_done_callback(self, callback):
        self._callbacks.append(callback)


class Task:
    def __init__(self, coro):
        self._coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future: Future):
        try:
            f = self._coro.send(future.result)
        except StopIteration:
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

        yield f
        print('connected')
        return f.result

    def send(self, data: bytes):
        f = Future()

        def callback():
            get_event_loop().selector.unregister(self._sock.fileno())
            result = self._sock.send(data)
            f.set_result(result)

        get_event_loop().selector.register(self._sock.fileno(), EVENT_WRITE, callback)

        yield f
        print('sent')
        return f.result

    def read(self, size: int = 4096):
        f = Future()

        def callback():
            get_event_loop().selector.unregister(self._sock.fileno())
            result = self._sock.recv(size)
            f.set_result(result)

        get_event_loop().selector.register(self._sock.fileno(), EVENT_READ, callback)

        yield f
        print('read')
        return f.result


class EventLoop:
    def __init__(self):
        self._selector = DefaultSelector()
        self._tasks = set()

    @property
    def selector(self) -> BaseSelector:
        return self._selector

    def create_task(self, task: Task):
        self._tasks.add(task)

    def run(self):
        while True:
            # try:
            events = self._selector.select()
            # except OSError:
            #     break
            for event_key, _ in events:
                event_key.data()


_GlobalEventLoop = EventLoop()


def get_event_loop() -> EventLoop:
    global _GlobalEventLoop
    return _GlobalEventLoop


def main():
    s = AsyncSocket()
    yield from s.connect('google.com', 80)
    yield from s.send('GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'.encode())
    yield from s.read()


if __name__ == '__main__':
    loop = get_event_loop()
    loop.create_task(Task(main()))
    loop.run()
