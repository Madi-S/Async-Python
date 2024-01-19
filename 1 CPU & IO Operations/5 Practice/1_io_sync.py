import time
import requests


URL = 'https://api.covidtracking.com/v1/us/current.json'
N_OF_REQS = 10


def main():
    begin = time.time()
    for i in range(N_OF_REQS):
        r = requests.get(URL)
        print(f'Request #{i + 1} status: {r.status_code}')
    print(f'{N_OF_REQS} requests took {time.time() - begin} seconds')


if __name__ == '__main__':
    main()

# 10 requests took 7.570430040359497 seconds
# 10 requests took 7.291452884674072 seconds
# 10 requests took 7.036351680755615 seconds
