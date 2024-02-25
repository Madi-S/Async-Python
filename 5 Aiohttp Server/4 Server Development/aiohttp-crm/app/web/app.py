from aiohttp.web import Application as AiohttpApplication, run_app as aiohttp_run_app, View as AiohttpView, Request as AiohttpRequest

from app.store import setup_accessors
from app.web.routes import setup_routes
from app.store.crm.accessor import CrmAccessor


class Application(AiohttpApplication):
    database: dict = {}
    crm_accessor: CrmAccessor | None = None


class Request(AiohttpRequest):
    @property
    def app(self) -> 'Application':
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request


app = Application()


def run_app():
    setup_routes(app)
    setup_accessors(app)
    aiohttp_run_app(app)
