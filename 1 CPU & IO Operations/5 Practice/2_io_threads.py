import time
import requests
from threading import Thread


URL = 'https://api.covidtracking.com/v1/us/current.json'
N_OF_REQS = 10


def make_request(i):
    r = requests.get(URL)
    print(f'Request #{i + 1} status: {r.status_code}')


def main():
    begin = time.time()
    threads = []
    for i in range(N_OF_REQS):
        thread = Thread(target=make_request, args=(i,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(f'{N_OF_REQS} requests took {time.time() - begin} seconds')


if __name__ == '__main__':
    main()

# Output is kinda affecte negatively
# 10 requests took 1.4218368530273438 seconds
# 10 requests took 1.4203569889068604 seconds
# 10 requests took 1.1852145195007324 seconds
