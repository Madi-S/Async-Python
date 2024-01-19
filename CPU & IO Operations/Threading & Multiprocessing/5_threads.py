import time
from threading import Thread


def t1():
    time.sleep(10)


thread_1 = Thread(target=t1)
thread_2 = Thread(target=t1)
thread_1.start()
thread_2.start()
thread_1.join()
thread_2.join()
