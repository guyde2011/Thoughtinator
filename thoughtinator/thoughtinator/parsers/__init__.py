
import typing

from thoughtinator.utils import logger, env, ansi
from thoughtinator.utils import ModuleLoader


class ParsersManager(ModuleLoader):

    def file_filter(self, filename: str) -> bool:
        return filename.startswith('parse_') \
            or filename.startswith('parser_') \
            or filename.endswith('_parser')

    def name_filter(self, funcname: str) -> bool:
        return funcname.startswith('parse_') \
            or funcname.startswith('parser_') \
            or funcname.endswith('_parser')

    def load_wrapper(self, parser, name: str):
        if not hasattr(parser, '__pfields__'):
            logger.warning(f'Parser {ansi.bold}{name}'
                           f'{ansi.unbold} is fieldless')
            return '', None

        logger.success(
            f'Loaded parser {ansi.bold(parser.__name__)} '
            f'from {ansi.bold(parser.__module__)} '
            f'for {ansi.bold(", ".join(parser.__pfields__))}')
        return parser, parser.__pfields__

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

if __name__ == 'thoughtinator.parsers':
    parser.load_modules(env.root / 'thoughtinator' / 'parsers')
