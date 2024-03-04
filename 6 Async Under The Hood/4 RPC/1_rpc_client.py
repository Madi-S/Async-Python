import queue
import random
from faker import Faker
from typing import Any
from dataclasses import dataclass

# from './../3 Event Loop Implementation/main.py' import sleep
from time import sleep


faker = Faker()
faker.seed(0)
tasks_queue = queue.Queue()


@dataclass
class RpcTask:
    handler: str
    method: str
    value: Any


def client_payload():
    while True:
        if random.randint(0, 1) == 0:
            task = RpcTask(
                handler='fibonacci_generator',
                method='calculate',
                value=random.randint(100, 10000)
            )
        else:
            task = RpcTask(
                handler='neural_analyzer',
                method='polarity',
                value=faker.sentence()
            )
        tasks_queue.put(task)
        print(f'New item was added to queue: {task}')
        yield from sleep(0.5)
