from .server import ServerEndpoint  # noqa: F401

from typing import Callable


def run_server(host: str, port: int, publish: Callable):
    """ Runs the upload server on a given host with a given publish function
    :type host: str
    :param host: the server's host/ip

    :type port: int
    :param port: the server's port

    :type publish: Callable
    :param publish: the publish function to use to publish uploaded samples
    """
    se = ServerEndpoint(publish)
    se.run(host, port)
