from flask import Flask

from typing import List, Tuple, TYPE_CHECKING


class FlaskEndpointMeta(type):
    @classmethod
    def __prepare__(mc, name, bases, **kwargs):
        class Router:
            def __init__(self):
                self._routes: List[Tuple] = []

            def route(self, *args, **kwargs):
                def mk_route(func):
                    self._routes.append((args, kwargs, func.__name__))
                    return func
                return mk_route
        router = Router()
        return {'__router__': router, 'route': router.route}


class FlaskEndpoint(metaclass=FlaskEndpointMeta):

    def __init__(self, name: str, **kwargs):
        self.app = Flask(name, **kwargs)
        for args, kwargs, name in self.__class__.__router__._routes:
            self.app.route(*args, **kwargs)(getattr(self, name))

    def run(self, host: str, port: int):
        self.app.run(host, port)

    def test_client(self):
        return self.app.test_client()
