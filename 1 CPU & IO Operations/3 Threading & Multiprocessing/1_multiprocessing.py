from multiprocessing import Process
import os


def info():
    print('Имя	модуля:',	__name__)
    print('Родительский	PID	процесса:',	os.getppid())
    print('PID	дочернего	процесса:',	os.getpid())


def f():
    info()
    pass


if __name__ == '__main__':
    info()
    p = Process(target=f)
    p.start()
    p.join()
