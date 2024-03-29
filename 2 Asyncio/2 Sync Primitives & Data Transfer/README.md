# Sync Primitives & Data Transfer / Примитивы Синхронизации и Обмена Данных

Это механизмы, которые ограничивают доступ к ресурсам и возможностям внутри асинхронного приложения. Обратите внимание, что все представленные способы синхронизации не предназначены для использования внутри тредов.

## Lock

Простейший механизм синхронизации, аналог Mutex в других ЯП. Пример - у нас есть пачка чипсов. Единовременно только 1 рука может находиться внутри пачки. Lock гарантирует эксклюзивный доступ к общим ресурсам, в нашем случае - к чипсам.

Смотри `1_lock.py`

## Event

Он используется для сигнализации короутин о неком событии. Пусть у нас есть 2 функции: `run` - она ждет события с помощью `await event.wait()`, `wait_and_set` - порождает событие и сигнализирует об этом ожидающую короутину.

Смотри `2_event.py`

В итоге при запуске кода получим: запускается короутина `wait_and_set` и засыпает на секунду, основная короутина `run` начинает ждать на событие `event`, короутина `wait_and_set` просыпается через секунду и вызывает `event.set()`, основная короутина `run` просыпается и программа завершается. А если же вызвать `event.set()`, а затем сразу `await event.wait()`, то событие уже произойдет и выполнение не остановится.

Другой более сложный пример: допустим, что необходимо написать планироващик, который просыпается раз в период времени `timer` и запукает `_worker`. На планировщик налагаются дополнительные условия - `_worker` может выполнять дольше, чем период времени `timer`, при этом планироващик не должен сбиваться, а также при остановке планироващика нужно дождаться выполнения всех запущенных задач.

Смотри `3_scheduler.py`

## Semaphore

Еще один способ синхронизации, но завязанный на счетчик. Например, надо ограничить количество единовременных обработок запросов в базу некоторым числом - например, 10.

Смотри `4_semaphore.py`

Одновременно доступ к асинхроному коду получают только две короутины, а остальные блокируются. То есть, исполнение кода будет занимать в N раз меньше, где N - параметр в `asyncio.Semaphore(N)` - количество одновременно исполняющихся запросов.

## Queue

Очередь - базовая структура данных, позволяющая реализовать принцип работы FIFO (first in first out). Может быть реализована поверх массива или связного списка.

Например, есть начальник и 3 подчиненных. Начальник создает задачи, а работники разбирают и выполняют их по мере возможности. Короутины worker'ы master будут обмениваться данными друг с другом через `asyncio.Queue`.

Смотри `5_queue.py`

Кроме обычной очереди, в библиотеке есть очередь с приоритетом - PriorityQueue. Она нужно, если мы хотим обработать какой-то тип событий раньше, чем остальные. Например, в очереди очень много задач, но появилась необходимость выполнить что-то прямо сейчас.

## Context Var

Контекстные переменные имеют свое значение для разных мест вызова приложения. Они изначально поддерживают использование библиотеки asyncio.

Смотри `6_global.py` и `7_context_var.py`

Пример использования контекстных переменных - у нас есть HTTP-сервер, где на каждый запрос мы ходим в одну или несколько баз данных, делаем запросы в сеть. Все эти операции мы логируем и сохраняем. Сервер у нас асинхронный, и в разные моменты времени исполняются операции из разных запросов. Мы хотим помечать при логировании, к какому конкретному запросу относится та или иная строчка служебной информациии. Благодаря `ContextVar` мы можем каждому запросу присваивать уникальный идентификатор и дописывать его к каждой записи логов. Теперь при необходимости мы сможем любым известным нам способом отфильтровать "простыню из информации" и провести свои исследования в подозрительных случаях.
