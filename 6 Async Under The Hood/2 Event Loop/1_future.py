import socket
import selectors

from examples.coroutines.future import Future


class Fetcher:
    def __init__(self, selector: selectors.DefaultSelector):
        self._selector = selector

    def _connect(self, host: str, port: int):
        sock = socket.socket()
        sock.setblocing(False)

        try:
            sock.connect((host, port))
        except BlockingIOError:
            pass

        f = Future()

        def connected():
            print('connected')
            self._selector.unregister(sock)
            f.set_result(None)

        # регистрируем событие EVENT_WRITE на нашем сокете
        self._selector.register(sock, selectors.EVENT_WRITE, connected)
        # делаем yield нашей короутины
        yield f
        # возвращаем уже подключенный сокет
        return sock
