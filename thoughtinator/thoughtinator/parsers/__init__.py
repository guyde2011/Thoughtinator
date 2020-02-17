import functools
import typing

class ParsersManager:
    def of(self, *fields: str):
        if typing.TYPE_CHECKING:
            def parser_decorator(parser):
                return parser
        else:   
            def parser_decorator(parser):
                setattr(parser, '__pfields__', fields)
                return parser
        return parser_decorator
        
parser = ParsersManager()
