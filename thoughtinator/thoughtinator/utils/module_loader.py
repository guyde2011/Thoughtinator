import importlib
import sys

from . import logger, ansi


class ModuleLoader:
    def __init__(self):
        self._comps: dict = {}

    def __contains__(self, field: str) -> bool:
        return field in self._comps

    def __getitem__(self, field: str):
        return self._comps[field]

    def bind(self, name: str):
        sys.modules[name] = self  # type: ignore

    def name_filter(self, funcname: str):
        return not funcname.startswith('_')

    def file_filter(self, filename: str):
        return not (filename.startswith('_') or filename.startswith('.'))

    def load_wrapper(self, member, name: str):
        return member, [name]

    def load_modules(self, path: str):
        from . import env
        folder = env.root / path.replace('.', '/')
        logger.info(f'Loading modules from {ansi.bold(folder)}')
        for file in folder.iterdir():
            if not file.name.endswith('.py'):
                continue
            name = file.name[:-3]
            if not self.file_filter(name):
                continue
            logger.info('Loading module {}'.format(
                ansi.bold(f"{path}.{file.stem}")))
            mod = importlib.import_module(
                f'{path}.{file.stem}', path)
            for member in mod.__dict__:
                if not self.name_filter(member):
                    continue

                value = mod.__dict__[member]
                wrapped, entries = self.load_wrapper(value, member)
                logger.info('Loaded member {}'.format(
                            ansi.bold(f"{member}")))
                for entry in entries:
                    self._comps[entry] = wrapped
