
import os
import json
import sys

from typing import Optional, List, Dict
from typing import cast

from pathlib import Path


class EnvHelper:
    def __init__(self):
        self.os: OSEnv = OSEnv()
        self.root: Path = Path(__file__).parent.parent.parent
        self.config: Dict = {}
        self.props: Dict[str, str] = {}

    def load_config(self):
        from thoughtinator.utils.logger import error
        config_env = self.os['CONFIG_FILE']
        if config_env is None:
            config_path = self.root / 'config.json'
        else:
            config_path = Path(config_env)

        if not config_path.exists():
            error(f'Config file {config_path} does not exist')
            sys.exit()

        with open(config_path) as config_file:
            config_data = config_file.read()
        try:
            self.config = json.loads(config_data)
        except BaseException as e:
            error(f'Malformed config.json file \n\t> {str(e)}')
            sys.exit()

    @property
    def options(self) -> List[str]:
        if 'options' not in self.config:
            return []
        return cast(List[str], self.config['options'])


class OSEnv:
    def __contains__(self, field: str) -> bool:
        return field in os.environ

    def __getitem__(self, field: str) -> Optional[str]:
        if field in self:
            return os.environ[field]

        return None
