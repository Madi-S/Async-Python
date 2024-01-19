import time


def countdown(id: int):
    i = 0
    begin = time.time()
    while i < 50_000_000:
        i += 1
    print(f'ID:	{id}	DONE	duration:	{time.time() - begin}')


COUNT = 2
begin = time.time()
print('START	calculation')
for i in range(COUNT):
    countdown(i + 1)
print(f'FINISH	calculation	duration:	{time.time() - begin}')
