import multiprocessing
import time


def countdown():
    i = 0
    begin = time.time()
    while i < 50_000_000:
        i += 1
    return f'ID:	{multiprocessing.current_process().name}	DONE	duration:	{time.time() - begin}'


def test():
    PROCESSES_COUNT = 2
    begin = time.time()
    print('START	calculation')
    with multiprocessing.Pool(PROCESSES_COUNT) as pool:
        results = list()
        for _ in range(PROCESSES_COUNT):
            results.append(pool.apply_async(countdown))
        for r in results:
            print(r.get())
    print(f'FINISH	calculation	duration:	{time.time() - begin}')


if __name__ == '__main__':
    multiprocessing.freeze_support()
    test()
