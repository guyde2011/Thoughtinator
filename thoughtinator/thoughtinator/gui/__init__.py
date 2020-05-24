from .gui import GUI  # noqa: F401


def run_server(host: str, port: int, api_host: str, api_port: int):
    GUI(api_host, api_port).run(host, port)
