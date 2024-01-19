import time
from threading import Thread


N_OF_OPERATIONS = 10


def countdown(index):
    i = 0
    begin = time.time()
    while i < 5_000_000:
        i += 1
    print(f'Operation #{index + 1} took {time.time() - begin} seconds')


def main():
    begin = time.time()
    threads = []
    for i in range(N_OF_OPERATIONS):
        thread = Thread(target=countdown, args=(i,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(f'{N_OF_OPERATIONS} operations took {time.time() - begin} seconds')


if __name__ == '__main__':
    main()

# 10 operations took 1.8038716316223145 seconds
# 10 operations took 1.7974016666412354 seconds
# 10 operations took 1.7833364009857178 seconds
