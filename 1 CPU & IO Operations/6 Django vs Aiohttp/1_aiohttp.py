import time
import asyncio

from aiohttp import web


async def handle(request):
    await asyncio.sleep(0.2)  # io bound operation simulation
    return web.Response(text='Hello Application')


app = web.Application()
app.add_routes([
    web.get('/', handle),
    web.get('/home', handle)
])

if __name__ == '__main__':
    web.run_app(app, port=8000, host='0.0.0.0')
