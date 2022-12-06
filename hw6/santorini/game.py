"""Santorini game manager module"""

from santorini.board import SantoriniBoard

class SantoriniGame:
    """Santorini game manager class"""

    def __init__(self, **kwargs) -> None:
        self._board = SantoriniBoard(5)
        self._players = []

    def run(self) -> None:
        """Run the game"""
        print(self._board)
