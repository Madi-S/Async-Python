from threading import Thread


data = dict()


def t1():
    data['t1'] = True
    print(data)


def t2():
    data['t2'] = True
    print(data)


print(data)
thread_1 = Thread(target=t1)
thread_2 = Thread(target=t2)
thread_1.start()
thread_2.start()
thread_1.join()
thread_2.join()
print(data)

# >>> {}
# >>> {'t1': True}
# >>> {'t1': True, 't2': True}
# >>> {'t1': True, 't2': True}
