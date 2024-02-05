from dataclasses import dataclass


class Headers:
    accept: str
    accept_encoding: str
    host: str
    user_agent: str
    x_amzn_trace_id: str | None = None


@dataclass
class GetResponse:
    args: dict
    headers:	Headers
    origin: str
    url: str
