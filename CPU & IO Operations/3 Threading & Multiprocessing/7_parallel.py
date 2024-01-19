import time
from threading import Thread


def countdown(id: int):
    i = 0
    begin = time.time()
    while i < 50_000_000:
        i += 1
    print(f'ID:	{id}	DONE	duration:	{time.time() - begin}')


print('START	calculation')
begin = time.time()
t1 = Thread(target=countdown, args=(1,))
t2 = Thread(target=countdown, args=(2,))
t1.start()
t2.start()
t1.join()
t2.join()
print(f'FINISH	calculation	duration:	{time.time() - begin}')
