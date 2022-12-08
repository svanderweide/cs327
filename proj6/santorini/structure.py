

class SantoriniStructure:

    def __init__(self) -> None:
        self._level = 0

    def build(self) -> None:
        self._level += 1

    def __str__(self) -> str:
        return f'{self._level}'
