# src/halter/core/models.area.py

"""Module describing area types"""

from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class Area:
    name: str = ""
    description: str = ""
    num: int = 1
