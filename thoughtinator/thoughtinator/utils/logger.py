from typing import List, Callable, Any, Optional

from thoughtinator.utils import ansi


class LogFunction:
    def __init__(
        self,
        require: List[str] = [],
        forbid: List[str] = [],
        format: Optional[Callable[[str], str]] = None
    ):
        """
        :type require: a list of strings
        :param require: a list of required options for this logging function

        :type forbid: a list of strings
        :param forbid: a list of forbidden options for this logging function

        :type format: (str => str) or None
        :param format: a formatting function for the logger
        """

        self.require: List[str] = require or []
        self.forbid: List[str] = forbid or []
        self.format: Optional[Callable[[str], str]] = format

    def log(self, message: str, *, func: Callable[[str], Any]):
        """
        Logs a string given a message and a printing function
        :type message: str
        :param message: the message to print

        :type func: str => Any
        :param func: an output function

        :rtype: None
        """
        from thoughtinator.utils import env
        for entry in self.require:
            if entry not in env.options:
                return

        for entry in self.forbid:
            if entry in env.options:
                return
        format = self.format or (lambda x: x)
        func(format(message))

    def __call__(
        self,
        message: str = None,
        *,
        require: List[str] = [],
        forbid: List[str] = [],
        format: Optional[Callable[[str], str]] = None,
        func: Callable[[str], Any] = print,
    ) -> 'LogFunction':
        """ Used to log a message or to add more restrictions to the logger
        :type message: string or None
        :param message: the message to log

        :type require: a list of strings
        :param require: the required options for this log to show

        :type forbid: a list of strings
        :param forbid: the forbidden options for this log to show

        :type func: (str => str) or None
        :param func: a printing function for logged strings

        :rtype: a log function with the given parameters
        """

        format = format or self.format

        lf: LogFunction = \
            LogFunction(self.require + require, self.forbid + forbid, format)

        if message is not None:
            lf.log(message, func=func)

        return lf


info = LogFunction(
    require=['info'],
    format=lambda s: f'{ansi.blue}[INFO] {s}{ansi.white}'
    )

success = LogFunction(
    require=['success'],
    format=lambda s: f'{ansi.green}[SUCCESS] {s}{ansi.white}'
    )

error = LogFunction(
    forbid=['hide-errors'],
    format=lambda s: f'{ansi.red}[ERROR] {s}{ansi.white}'
    )

warning = LogFunction(
    require=['warning'],
    format=lambda s: f'{ansi.yellow}[WARNING] {s}{ansi.white}'
    )
