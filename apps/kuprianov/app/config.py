"""
kuprianov app configuration skeleton
"""

from dataclasses import dataclass
import os


@dataclass
class KuprianovConfig:
    enabled: bool = bool(int(os.getenv("KUPRIANOV_ENABLED", "1")))


config = KuprianovConfig()

