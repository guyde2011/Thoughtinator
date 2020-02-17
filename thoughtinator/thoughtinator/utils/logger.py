from typing import List, Callable, Any, Optional
import functools
from thoughtinator.utils import ansi


class LogFunction:
    def __init__(
        self, 
        require: List[str] = [], 
        forbid: List[str] = [], 
        format: Optional[Callable[[str], str]] = None):
        self.require: List[str] = require or []
        self.forbid: List[str] = forbid or []
        self.format: Optional[Callable[[str], str]] = format
    
    def log(self, message: str, *, func: Callable[[str], Any]):
        from thoughtinator.utils import env
        for req in self.require:
            if req not in env.options:
                return 
        
        for fbd in self.forbid:
            if fbd in env.options:
                return
        format = self.format or (lambda x: x)
        func(format(message))

    def __call__(self, 
        message: str = None, 
        *, 
        require: List[str] = [], 
        forbid: List[str] = [], 
        format: Optional[Callable[[str], str]] = None,
        func: Callable[[str], Any] = print,
        ) -> Optional['LogFunction']:

        format = format or self.format
 
        lf: LogFunction = \
            LogFunction(self.require + require, self.forbid + forbid, format)
        
        if message is None:
            return lf


        lf.log(message, func=func)
        return None

info = LogFunction(
    require = ['info'], 
    format = lambda s: f'{ansi.blue}[INFO] {s}'
    )
error = LogFunction(
    forbid = ['hide-errors'], 
    format = lambda s: f'{ansi.red}[ERROR] {s}'
    )
warning = LogFunction(
    require = ['warning'],
    format = lambda s: f'{ansi.yellow}[WARNING] {s}')