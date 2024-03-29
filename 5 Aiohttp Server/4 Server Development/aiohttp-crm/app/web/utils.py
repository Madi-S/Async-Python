from aiohttp.web_response import Response
from aiohttp.web import json_response as aiohttp_json_response


def json_response(data=None, status: str = 'ok') -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(data={
        'status': status,
        'data': data
    })


def error_json_response(
    http_status: int,
    status: str = 'error',
    message: str | None = None,
    data: dict | None = None
):
    if data is None:
        data = {}
    return aiohttp_json_response(
        status=http_status,
        data={
            'status': status,
            'message': str(message),
            'data': data
        }
    )
