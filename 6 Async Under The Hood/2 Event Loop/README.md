# Event Loop

## Введение

### Генераторы

Event Loop в Python возможен благодаря генераторам. Давайте вспомним, что это такое. Основный признак генератора в Python - инструкция `yield`. Ее наличие показывает, что функция является генератором.

Пример генератора:

```python
def my_generator():
    print('i am generator and i am being executed')
    a = 1
    yield a
    a += 1
    yield a

g = my_generator()
print(g.gi_frame.f_lasti)
# >>> -1

g.send(None)
print(g.gi_frame.f_lasti)
# >>> 6
```

### Future

Это сущность, которая является обещанием чего-то в будущем. Например, мы хотим подключитсья к сокету: создадим `Future` сейчас и отдадим ее тоже сейчас. А значение в нее положим когда-то потом - когда подключение выполниться.

Суть `Future` в том, что мы разделяем факт происхождения события и момент использования этого факта.

Пример использования Future.

Смотри `1_future.py`

У нас есть функция `Fetcher._connect`, которая является генератором и пытается установить соединение с хостом. Мы создади объект `f = Future()` и скажем, что в нем появится значение в тот момент, когда мы осуществим успешное подключение.

Зарегистрируем на селекторе наш файловый дескриптор, передадим туда `on_connected` и в этом `on_connected` установим результат. Например, `f.set_result(None)`. Этот момент будет означать, что `Future` завершилась с каким-то результатом, в данном случае - None.

Давайте посмотрим, как устроена эта `Future`:

```python
class Future:
    def __init__(self, name: str):
        self.result = None
        self._callbacks = []
    
    def add_done_callback(self, fn):
        self._callbacks.append(fn)
    
    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)
```

В момент вызова `self.set_result` мы записываем результат нашей `Future` и вызываем все callback-функции, которые были зарегистрированы на эту `Future`. То есть, мы можем при создании `Future` сказать: когда завершиться - то есть, когда появится какой-то результат - выполни такие-то действия.

Эти действия можно добавлять с помощью `add_done_callback`. Мы регистрируем какой-то callback на `Future`, почти так же, как регистрировали callback на сокет. И в тот момент, когда `Future` завершится, мы просто последовательно вызовем эти callback-функции.

В `_connect` мы еще не вызвали никаких `add_done_callback`, просто создали `Future` и сделали ее `yield`.

Если мы сейчас начнем просто дергать `.send()` у генератора `fetcher()`, то в первый раз нам вернется `Future`, а во второй раз вернется сокет, который может быть еще не готов к записи. Нам нужно, чтобы второй раз `.send()` дергался при наступлении события `EVENT_WRITE` или в callback-функции `connected`, которая как раз и будет вызвана при наступлении `EVENT_WRITE`.

Но для такой логики нам не хватает некоторой управляющей конструкции. Кто-то должен следить, выполнилась ли `Future` и продолжать выполнение генератора `_connect`

### Task

Пример Task:

```python
from examples.coroutines.futre import Future

class Task:
    def __init__(self, coroutine):
        self.coroutine = coroutine
        f = Future()
        f.set_result(None)
        self.step(f)
    
    def step(self, future: Future):
        try:
            next_future = self.coroutines.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)
```
