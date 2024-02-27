import socket
import selectors


# выбираем наилучший механизм операционной системы по работе с событиями
selector = selectors.DefaultSelector()
sock = socket.socket()  # создаем TCP-сокет
sock.setblocking(False)  # делаем его неблокирующим

try:
    # асинхронно устанавливаем TCP-соединение с abcd.com
    sock.connect(('abcd.com', 80))
except BlockingIOError:
    pass


# объявляем callback, который будет вызван при разблокировки сокета на запись.
# То есть после установки TCP-соединения
def connected():
    selector.unregister(sock)
    print('connected!')


# подписываемся на событие разблокировки сокета на запись
selector.register(sock, selectors.EVENT_WRITE, connected)


def loop():
    while True:  # event-loop
        # заблокируется, пока не произойдет какое-то зарегистрированное событие
        events = selector.select()
        for event_key, event_mask in events:
            # event_mask - это число 1, 2 или 3. То есть 01, 10 или 11 в двоичном виде.
            # 01 - selectors.EVENT_READ, 10 - selectors.EVENT_WRITE, 11 - selectors.EVENT_READ | selectors.EVENT_WRITE

            # event_key - информация о зарегистрированном сокете и о callback
            callback = event_key.data

            # callback - наша функция connected
            callback()


if __name__ == '__main__':
    loop()  # запускаем вечный event-loop
