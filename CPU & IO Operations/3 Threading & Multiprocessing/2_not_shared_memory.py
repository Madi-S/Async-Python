from multiprocessing import Process
import os


data = dict()


def info():
    print('PID	процесса:',	os.getpid())
    print('data:',	data)


def p1():
    data['p1'] = True
    info()


def p2():
    data['p2'] = True
    info()


if __name__ == '__main__':
    info()
    proc_1 = Process(target=p1)
    proc_1.start()
    proc_2 = Process(target=p2)
    proc_2.start()
    proc_1.join()
    proc_2.join()
    info()
