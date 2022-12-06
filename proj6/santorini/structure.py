"""Santorini game structure module"""

class SantoriniStructure:
    """Santorini game structure class"""

    def __init__(self, level=0) -> None:
        self._level = level

    def __str__(self) -> str:
        return f'{self._level}'
