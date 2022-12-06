"""Santorini game worker module"""

class SantoriniWorker:
    """Santorini game worker class"""

    def __init__(self, player, symbol=' ') -> None:
        self._player = player
        self._symbol = symbol

    def __str__(self) -> str:
        return f'{self._symbol}'
