"""
wildtantra app configuration skeleton
"""

from dataclasses import dataclass
import os


@dataclass
class WildTantraConfig:
    example_flag: bool = bool(int(os.getenv("WT_EXAMPLE_FLAG", "1")))


config = WildTantraConfig()

