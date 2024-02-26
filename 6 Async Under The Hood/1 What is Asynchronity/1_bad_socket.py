import socket


def send_request():
    request = f'GET abcd.com HTTP/1.0\r\nHost: abcd.com\r\n\r\n'.encode('ascii')
    # создаем TCP сокет, файловая система выделяет файловый дескриптор
    sock = socket.socket()
    sock.setblocking(False)

    try:
        sock.connect(('abcd.com', 80)) # на этом этапе производится асинхронный TCP-handshake
    except BlockingIOError:
        # выкинется ошибка о том, что соединение еще устанавливается
        pass

    while True:
        try:
            sock.send(request) # пишем данные в сокет
            break
        except BlockingIOError:
            # сокет может быть уже заполнен
            pass
        except OSError:
            # соединение в сокете еще не установлено - выполняется TCP-handshake
            pass

    data = b''
    while True:
        try:
            # читаем данные из сокета, если данных нет, то выкинется ошибка
            data += sock.recv(4096)
            break
        except BlockingIOError:
            # данные могут еще не прийти, сокет будет заблокирован
            pass

        print(data.decode('ascii')) # нам приходят байты и их нужно декодировать

if __name__ == '__main__':
    send_request()
