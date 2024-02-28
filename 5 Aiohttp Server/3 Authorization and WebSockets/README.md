# Authorization and WebSockets

## Введение

Почти любое современное приложение получает данные из сторонних источников (базы данных, сторонние API, S3-хранлища и т.д.) и умеют в авторизацию/регистрацию. Разберем подробнее как добавить эти вещи к себе.

## Authorization

Это общее слово для процесса, состоящего из трех частей: идентификация -> аутентификация -> авторизация.

Идентификация проверяет, предоставлены ли данные и валидны ли они.
Аутентификация проверяет, правильны ли эти данные, например, есть ли такая пара логин/пароль в базе данных.
Авторизация проверят, если у пользователя с этими данными доступ к запрашиваему ресурсу.

### Cookie Auth

Чаще всего для авторизации пользователей используется метод, построенный на куки-файлах.

Разберем такой упрощенный алгоритм:

1. Пользователь отправляет пару логин/пароль на /user/login.
2. Сервер ищет совпадание в предоставленной паре в базе данных или конфигурационных файлах и находит ее.
3. Сервер собирает нужные данные о пользователе в объект и превращает его в json.
4. Сервер шифрует json-данные симметричным шифрованием.
5. Сервер добавляет заголовок Set-Cookie: <название куки>=<зашифрованные данные> и отправляет ответ.
6. Браузер пользователя сохраняет запись из заголовка Set-Cookie в своем хранилище.
7. Браузер пользователя отправляет заголовок Cookie с этими данными при каждом следующем обращении.
8. Сервер достает данные из заголовка Cookie и дешифрует их своим ключом.
9. При успешной расшифровке севрвер убеждается, что этот пользователь авторизован, ведь ключ для шифрования есть только у сервера.

Для работы по данному алгоритму в aiohttp существует библиотека для работы с сессиями aiohttp_session. Библиотека умеет хранить данные о сессии в разных типах хранилищ:

-   SimpleCookieStorage хранит информацию об авторизованном пользователе прямо в теле Cookie Value. Предназначено только для удобства тестирования и крайне небезопасно во всех остальных случаях.

-   EncryptedCookieStorage хранит информацию так же, как и SimpleCookie, но в зашифрованном виде. Используется симметричное шифрование 32-байтным ключом.

-   RedisStorage, MemcachedStorage, MongoStorage - хранят информацию в существующих хранилищах, а в Cookie Value хранит только уникальный ключ для ее получения. Требует настройку окружения.

## Внешние источники

Для работы с внешними источниками обычно выделяются три сущности.

### Accessor

Умеет образаться к сторонним источника данных и умеет преобразовывать полученные данные в нужный вид.

Например, можно сделать accessor для доступа к PostgreSQL или к внешнему API. Также, accessor обычно умеет выполнять подключение и отключение от внешнего источника данных.

Пример метода rfc-accessor'а, который ходит к внешнему API по RFC, получает данные и преобразует их к заданной схеме:

```python
async def get_date(self, proxy_number: str):
    result = await self.store.rfc.call(
        'Z_F_HR_LK2_GET_CALC_DATE', IV_PERNR=proxy_number
    )
    return GetDateInfo.Schema().load(result)
```

### Store

Набор всех accessor'ов из всех мест в приложении. Он инициализируется при старте приложения и по очереди подключает каждый accessor, тем самым обеспечивая их боеготовность:

```python
self.db = AioMongoAccessor(self, name='db')
self.qdb = TarantoolAccessor(self, name='qdb')
self.pgdb = PgAccessor(self, name='pgdb')
self.consul = ConsulAccessor(self, name='consul')
```

### Manager

Помогает вынести большие куски логики из View и переиспользовать их. Обычно manager включает в себя обращение сразу к нескольким accesor'ам. Например, при регистрации нового пользователя manager может сначала создать пользователя с помощью posgresql-accessor'а, а потом добавить ему сессию, воспользовавшись redis-accessor'ом.

## Дополнительные компоненты

### Signals

Отдельно можно рассмотреть ConnectAccessor - это наслденик базового класса Accessor, но обладающий методами `connect` и `discconect`. Сервер может вызвать метод `connect` при запуске и метод `disconnect` при завершении работы. Это позволит запустить сервер с уже готовым подключением к базе данных и освободить ресурсы после отключения. Ниже мы рассмотрим, как вызывать эти методы в нужные моменты.

Aiohttp_signals позволяют выполнять какую-то логику при включении сервера, выключении и чистке ресурсов. Например:

```python
app.on_startup.append(mongo.accessor.connect())
app.on_shutdown.append(mongo.accessor.disconnect())
```

Теперь при запуске приложения будет выполнено подключение к MongoDB, а при его завершении выполнено отключение.

### Logger

Это объект, который, как ни странно, умеет писать логи. В проекте обычно сущствует один root-logger, от которого наследуют все остальные. У logger есть ряд составных частей:

-   сам logger - задает точку входа в приложение и уровень логгирования
-   handler - решает, куда записать логи (сообщения), например, вывести в stdout, файл или отправить по электронной почте
-   filter - пропускает к записи только часть логов, фильтруя их по заданным критериям
-   formatter - определяет формат логов

Каждый логгер в цепочке наследников может определять собственную реализацию каждой части.

Существует такое понятие как уровень логгирования. Обычно есть такие уровни: DEBUG, INFO, WARNING, ERROR. Они фильтруют и не записывают в логи события, которые произошли на более низком уровне. С помощью `logging.basicConfig()` можно указать общий уровень логгирования. Для прода лучше логгировать на ошибки и предупреждения, а для локального тестирования можно поставить режим DEBUG - это предотвратит раздувание лог-файлов.

Пример создания logger'а:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = getLogger()
logger.debug('will not be written out')
logger.info('will be captured by logger')
```

## WebSockets

Мы ранее рассматривали websockets, выступая в роли клиента. Пришло время разобраться в этом деле из роли хоста. К облегчению всех бэкенд-разработчиков, aiohttp уже имеет поддержку сокетов из коробки.

### Как работать с сокетами в aiohttp server?

1. Нужно сделать View и Route - обычные View и Route, ничего особенного.
2. Во View нужно создать `web.WebSocketResponse`. Это объект ответа, почти такой же, как `web.Response`, только с предустановленными статусом ответа (101) и специальными заголовками (например, Connection-Upgrade), а также дополнительными методами.
3. У этого экземпляра `web.WebSocketResponse` нужно выполнить метод `.prepare()`. Как мы помним, этот метод записывает данные ответа в сокет, то есть отправляет ответ клиенту. В момент выполнения этого шага, ответ на апгрейд соединения уже послан пользователю, а мы все еще выполняем код View. С этого момента экземпляр `web.WebSocketResponse` выполняет роль соединения.
4. Соединение прервется в момент, когда мы закроем его самостоятельно или закончим выполнение этого View, поэтому есть смысл бесконечно ждать нового сообщения из этого соединения с помощью асинхронного цикла чтения.
5. Когда нужно отправить какое-то сообщение, мы можем вызвать у этого соединения метод `.push()`.
6. Когда нужно закрыть соединение, мы можем вызвать метод `.close()`.

Пример официальной документации aiohttp отлично демонстрирует этот алгоритм для одного соединения:

```python
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s', % ws.exception())

    print('websocket connection closed')
    return ws
```

Если же у нас несколько открытых одновременно соединений, можно просто держать их где-то в памяти приложения. Например, держать в виде словаря `{user_id: ws_connection}` и посылать сообщения по мере необходимости в нужные места.

### Структура websocket сообщения

WS-сообщение в aiohttp содержит два самых важных поля: `type` и `data`.

`type` - тип сообщения, бывает нескольких видов:

-   CONTINUATION - технический тип, сигнализирующий о продолжении предыдущей информации в этом фрагмменте
-   TEXT - сообщение с текстовой полезной нагрузкой
-   BINARY - сообщение с двоичной полезной нагрузкой
-   PING - технический тип для проверки соединения
-   PONG - технический тип для ответа на проверку соединения
-   CLOSE - технический тип, означающий закрытие соединения

Также существуют типы, используемые внутри aiohttp: CLOSING, CLOSED, ERROR, но нам вряд ли предоставится возможность их использовать.

`data` - полезная нагрузка сообщения, бывает текстовой и бинарной.

-   Бинарная нагрузка - некоторый набор байт, которые можно как-то использовать. Передача данных в бинарном виде обычно гораздо быстрее (из-за их меньшего размера), чем передача текстовых. Но стоит думать, что бинарные данные передаются как-то по-другому, чем текстовые - оба типа преобразуются в нолики и единички. Но при передаче бинарных данных на стороне приемника эти данные не декодируются в символы, а при передаче текстовых декодируются. Для работы с бинарными данными создано множество форматов, таких же, как xml и json, но для бит и байт. Например, гугловский, ProtoBuf.
-   Текстовая нагрузка - это текст. А в текст можно положить json-данные, что позволяет работать с веб-сокетами почти также, как с любым View.

### Как использовать нагрузку проще всего

Использовать текстовые сообщения, в каждое вкладывать json-нагрузку в виде словаря, обязательно содержащего ключ `kind`. По этому ключу можно понять, какой смысл несет это сообщение, и в коде задать соответствия типа и полей в нем.