# RPC

## Введение

Вы разрабатываете веб-сервис, который должен уметь три вещи:

-   производить какие-то тяжелые вычисления
-   работать с нейросетью
-   принимать запросы от клиентов на эти самые действия

Тяжелые вычисления и работа с нейросетью - объемные синхронные операции, поэтому вы решили купить два или больше серверов и разместить этот громоздкий код на них. Вы не стали отделять кодовые базы - на одной машине могут происходить как вычислительные операции, так и работы с нейросетью, пусть это и не максимально эффективно. Давайте называть такой синхронный сервер <i>Consumer</i> - он принимает задачи, которых может быть несколько

Отедльный сервер вы выделили под асинхронный сервер, который умеет принимать задачи от каких-то внешних клиентов, вызывать их на "синхронных" серверах, а затем возвращать результат. Будем называть его <i>Producer</i> - он посылает задачи и будет один.

Взаимодействие между Producer и Consumer можно настроить с помощью какого-нибудь высокоуровнего API - посылать команды по HTTP, парсить json и т.д. Но пока острой необходимости в этом нет, и вы решили, что будете просто устанавливать TCP-соединение из Consumer в Producer и посылать команды набором байт.

Например, так:

```
b'calculator calculate 2 + 2`
```

На сервере эта команда будет разбиваться по пробелам и интерпретироваться примерно так:

```
calculator.calculate('2', '+', '2')
```

Первым аргументом в команде идет название класса, calculator, вторым - название его метода, calculate (@staticmethod или @classmethod), а все остальные - это аргументы, которые будут отправлены в метод.

Такой формат обмена данными называется RPC - Remote Procedure Call - мы буквально вызываем какой-то метод какого-то класса, который находится на удаленном сервере. Соответственно, результат этого метода `calculator.calculate('2', '+', '2')` должен быть преобразован в строку, затем переведен в байты, а затем записан в сокет, из которого прешел запрос. Затем сокет должен быть закрыт, чтобы не держать соединение. Это сделано для упрощения задачи.

### Tasks

Кто-то внешний должен запрашивать выполнение задач у Producer, чтобы тот, в свою очередь, отправлял их в Consumer и ждал ответа. Обычно это какие-то запросы пользователей, но чтобы не поднимать свой асинхронный сервис, в этом задании мы сымитируем этот процесс.

Смотри `1_rpc_client.py`

## RabbitMQ RPC Client

### Зачем?

RPC через RabbitMQ используется, когда невозможно/очень сложно реализовать http-запрос. Например, вы реализуете взаимодействие с банком, и вам нужно вызвать метод сервера, который находится в контуре банка (сервер расположен на серверах банка во внутренней сети). Согласовать "дырку" в банк ооочень сложно и для этой операции нужно много обоснований. Поэтому более быстрым решением может быть внешний RabbitMQ, через который будет организовано взаимодействие, а запросы из контура банка во внешнюю сеть согласовываются намного проще, чем наоборот.

### Интерфейс пользователя-программиста

Для того, чтобы сделать запрос, нужно вызвать `await rpc.call()`. Переменные для вызова удаленной функции нужно передать в параметре `kwargs`:

```python
connection = await aio_pika.connect(os.getenv('RABBITMQ_URL'))
async with connection:
    channel = await connection.channel()
    rpc = await RPC.create(channel)
    print(await rpc.call('sleep', kwargs={'t': 3}))
```

Чтобы сделать RPC-сервер нужно:

```python
async def foo(t):
    pass

connection = await aio_pika.connect(os.getenv('RABBITMQ_URL'))
channel = await connection.channel()
rpc = await RPC.create(channel)
await rpc.register('foo', foo)
```

После регистрации функции-обработчика RPC должен начать принимать и выполнять запросы из очереди RabbitMQ.

Помимо интерфейса выше, RPC-клиент должен отвечать следующим требованиям:

-   Функция `call` должна возвращать результат, который вернула функция на удаленной стороне.
-   Функция `call` должна выбрасывать исключение, если время ожидания ответа истекло.
-   Если функция-обработчик упала с ошибкой, то нужно выбросить исключение на стороне клиента
