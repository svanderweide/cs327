"""
Santorini game driver module

Responsible for setting up, launching, and monitoring
the state of the game for termination conditions
"""

from santorini.board import SantoriniBoard
from santorini.constants import PLAYERS
from santorini.exceptions import SantoriniException

class SantoriniGame():

    def __init__(self, **kwargs) -> None:
        self._board = SantoriniBoard((5, 5))
        self._players = self._create_players(**kwargs)

    def _create_players(self, **kwargs):

        players = []
        for color in PLAYERS:
            strategy = kwargs.get(color)
            if strategy == 'human':
                pass
            elif strategy == 'random':
                pass
            elif strategy == 'heuristic':
                pass
            else:
                raise SantoriniException()
        return players

    def run(self) -> None:
        print(self._board)
