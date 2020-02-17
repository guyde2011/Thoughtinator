
import os
import json
import sys

from typing import Optional, List, cast

from pathlib import Path


class EnvHelper:
    def __init__(self):
        self.os: OSEnv = OSEnv()
        self.root: Path = Path(__file__).parent.parent.parent
        self.config: dict = {}
        
    def load_config(self) -> dict:
        from thoughtinator.utils.logger import error
        config_path = self.root / 'config.json'
        if not config_path.exists():
            error(f'Config file {config_path} does not exist')
            sys.exit()

        with open(config_path) as config_file:
            config_data = config_file.read()
        try:
            self.config = json.loads(config_data)
        except BaseException as e:
            error(str(e))
            
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