import asyncio
import aiohttp
from dataclasses import field
from typing import Optional, ClassVar, Type
from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE


@dataclass
class Headers:
    accept: str = field(metadata={'data_key': 'Accept'})
    accept_encoding: str = field(metadata={'data_key': 'Accept-Encoding'})
    host: str = field(metadata={'data_key': 'Host'})
    user_agent: str = field(metadata={'data_key': 'User-Agent'})
    x_amzn_trace_id: Optional[str] = field(
        default=None, metadata={'data_key': 'X-Amzn-Trace-Id'}
    )

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetResponse:
    args: dict
    headers: Headers
    origin: str
    url: str
    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


async def request() -> GetResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            data = await resp.json()
            res = GetResponse.Schema().load(data)
            return res


async def main():
    response = await request()
    print(response)


if __name__ == '__main__':
    asyncio.run(main())
