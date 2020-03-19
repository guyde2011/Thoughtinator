import pytest


class Patcher:

    def __init__(self, mp):
        self.mp = mp

    def patch(self, obj, member, func=lambda *a, **kw: None):
        buffer = []
        self.mp.setattr(obj, member, patched(buffer, func))
        return buffer

@pytest.fixture
def patcher(monkeypatch):
    return Patcher(monkeypatch)


def patched(buffer, func):
    def wrapped_func(*args, **kwargs):
        ret = func(*args, **kwargs)
        buffer.append((args, kwargs, ret))
        return ret
    return wrapped_func
