import selectors
from concurrent.futures import Future


class _:
    def send(self, sock, data: bytes):
        f = Future()

        def sent():
            self._selector.unregister(sock)
            sock.send(data)
            f.set_result(None)

        self._selector.register(sock, selectors.EVENT_WRITE, sent)
        yield f
        return None

    def read(self, sock):
        f = Future()

        def _read():
            self._selector.unregister(sock)
            data = sock.recv(4096)
            f.set_result(data)

        self._selector.register(sock, selectors.EVENT_READ, _read)
        chunk = yield f
        return chunk

    def read_all(self, sock):
        response = bytearray()
        chunk = yield from self._read(sock)
        while chunk:
            response += chunk
            chunk = yield from self._read(sock)
        return response.decode('ascii')
