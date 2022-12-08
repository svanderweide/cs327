from .exceptions import InvalidBuildException

class SantoriniStructure:

    def __init__(self) -> None:
        self._level = 0

    def build(self) -> None:
        if self._level == 4:
            raise InvalidBuildException()
        self._level += 1

    def reaches(self, other) -> bool:
        return other._level <= self._level + 1

    def __str__(self) -> str:
        return f'{self._level}'
