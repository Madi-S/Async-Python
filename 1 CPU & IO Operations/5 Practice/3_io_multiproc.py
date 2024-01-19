import time
import requests
from multiprocessing import Process


URL = 'https://api.covidtracking.com/v1/us/current.json'
N_OF_REQS = 10


def make_request(i):
    r = requests.get(URL)
    print(f'Request #{i + 1} status: {r.status_code}')


def main():
    begin = time.time()
    proocesses = []
    for i in range(N_OF_REQS):
        process = Process(target=make_request, args=(i,))
        process.start()
        proocesses.append(process)
    for process in proocesses:
        process.join()
    print(f'{N_OF_REQS} requests took {time.time() - begin} seconds')


if __name__ == '__main__':
    main()

# 10 requests took 2.679779291152954 seconds
# 10 requests took 1.8572652339935303 seconds
# 10 requests took 1.5269618034362793 seconds
