import asyncio
import aiohttp


async def request1():
    params = {'key1': 'value1', 'key2': 'value2'}
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as r:
            print(await r.read())
            print(await r.text())
            print(await r.json())
            print(r.status)
            print(r.headers)


async def request2():
    auth = aiohttp.BasicAuth('user', 'pass')
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get', auth=auth) as r:
            print(await r.text())


async def request3():
    async with aiohttp.ClientSession() as session:
        await session.get('http://httpbin.org/cookies/set?my_cookie=my_value')
        filtered = session.cookie_jar.filter_cookies('http://httpbin.org')
        print(filtered)


async def request4():
    json = {'key1': 'value1', 'key2': 'value2'}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://httpbin.org/post', json=json) as r:
            print(await r.text())


async def main():
    await request1()
    await request2()
    await request3()
    await request4()


if __name__ == '__main__':
    asyncio.run(main())
