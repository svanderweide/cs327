"""Santorini structure module"""

class SantoriniStructure():

    _limit_level = 3

    def __init__(self) -> None:
        self._level = 0

    def domed(self) -> bool:
        return self._level == SantoriniStructure._limit_level

    def build(self) -> None:
        self._level += 1

    def __str__(self) -> str:
        return f'{self._level}'
