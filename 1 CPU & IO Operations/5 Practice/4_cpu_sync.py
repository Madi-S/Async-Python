import time


N_OF_OPERATIONS = 10


def countdown(index):
    i = 0
    begin = time.time()
    while i < 5_000_000:
        i += 1
    print(f'Operation #{index + 1} took {time.time() - begin} seconds')


def main():
    begin = time.time()
    for i in range(N_OF_OPERATIONS):
        countdown(i)
    print(f'{N_OF_OPERATIONS} operations took {time.time() - begin} seconds')


if __name__ == '__main__':
    main()

# 10 operations took 1.7592382431030273 seconds
# 10 operations took 1.7389380931854248 seconds
# 10 operations took 1.7251458168029785 seconds
