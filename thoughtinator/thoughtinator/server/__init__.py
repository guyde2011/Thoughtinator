from .server import ServerEndpoint  # noqa: F401

from typing import Callable


def run_server(host: str, port: int, publish: Callable):
    se = ServerEndpoint(publish)
    se.run(host, port)
