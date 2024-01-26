import asyncio
import aiohttp
from yarl import URL
from bs4 import BeautifulSoup
from dataclasses import dataclass

from task import Task


MAX_DEPTH = 2
PASSED_URLS = set()


@dataclass
class FetchTask(Task):
    url: URL
    depth: int

    def parse(self, data: str) -> list['FetchTask']:
        if self.depth + 1 > MAX_DEPTH:
            return []
        soup = BeautifulSoup(data, 'lxml')
        res = []
        for link in soup.find_all('a', href=True):
            new_url = URL(link['href'])
            if new_url.host is None and new_url.path.startswith('/'):
                new_url = URL.build(
                    scheme=self.url.scheme,
                    host=self.url.host,
                    path=new_url.path,
                    query_string=new_url.query_string
                )
                if new_url in PASSED_URLS:
                    continue
                res.append(FetchTask(url=new_url, depth=self.depth + 1))
                PASSED_URLS.add(new_url)
        return res

    async def perform(self, pool):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                print(self.url, response.status)
                data = await response.text()
                res: list[FetchTask] = await asyncio.get_running_loop(). \
                    run_in_executor(None, self.parse, data)
                for task in res:
                    await pool.put(task)
