
from typing import Any

red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
blue = '\033[94m'
white = '\033[97m'


def bold(message: Any) -> str:
    return f'\033[1m{message}\033[22m'


__all__ = ['red', 'green', 'yellow', 'blue', 'white', 'bold', ]
