
import os

from typing import Optional

class EnvHelper:
    def __init__(self):
        self.os = OSEnv()

class OSEnv:
    def __contains__(self, field: str) -> bool:
        return field in os.environ

    def __getitem__(self, field: str) -> Optional[str]:
        if field in self:
            return os.environ[field]

        return None