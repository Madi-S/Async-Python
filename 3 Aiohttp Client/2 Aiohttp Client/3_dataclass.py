import asyncio
import aiohttp
from dataclasses import dataclass


@dataclass
class Headers:
    accept: str
    accept_encoding: str
    host: str
    user_agent: str
    x_amzn_trace_id: str | None = None


@dataclass
class GetResponse:
    args: dict
    headers: Headers
    origin: str
    url: str


async def request() -> GetResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            data = await resp.json()
            headers_dict = data.get('headers', {})
            headers = Headers(
                host=headers_dict['Host'],
                accept=headers_dict['Accept'],
                user_agent=headers_dict['User-Agent'],
                accept_encoding=headers_dict['Accept-Encoding'],
                x_amzn_trace_id=headers_dict['X-Amzn-Trace-Id']
            )
            res = GetResponse(
                headers=headers,
                url=data['url'],
                args=data['args'],
                origin=data['origin']
            )
            return res


async def main():
    response = await request()
    print(response)


if __name__ == '__main__':
    asyncio.run(main())
