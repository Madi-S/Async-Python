import time
from multiprocessing import Process


N_OF_OPERATIONS = 10


def countdown(index):
    i = 0
    begin = time.time()
    while i < 5_000_000:
        i += 1
    print(f'Operation #{index + 1} took {time.time() - begin} seconds')


def main():
    begin = time.time()
    proocesses = []
    for i in range(N_OF_OPERATIONS):
        process = Process(target=countdown, args=(i,))
        process.start()
        proocesses.append(process)
    for process in proocesses:
        process.join()
    print(f'{N_OF_OPERATIONS} operations took {time.time() - begin} seconds')


if __name__ == '__main__':
    main()

# 10 operations took 0.5140461921691895 seconds
# 10 operations took 0.5097615718841553 seconds
# 10 operations took 0.474041223526001 seconds
