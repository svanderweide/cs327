"""
Santorini game driver module

Responsible for setting up, launching, and monitoring
the state of the game for termination conditions
"""

from santorini.board import SantoriniBoard
from santorini.player import SantoriniPlayerBase
from santorini.player_human import SantoriniPlayerHuman
from santorini.player_random import SantoriniPlayerRandom
from santorini.player_heuristic import SantoriniPlayerHeuristic

from santorini.constants import PLAYERS
from santorini.exceptions import SantoriniException

class SantoriniGame():

    def __init__(self, **kwargs) -> None:
        self._players = self._create_players(**kwargs)
        self._board = SantoriniBoard((5, 5))

    def _create_players(self, **kwargs) -> list[SantoriniPlayerBase]:

        players = []

        # hard-coded for 2-player CLI version
        cols = ['white', 'blue']

        # rest is not hard-coded for 2-player CLI version
        # but depends on the hard-coded values for structure
        strategies = {col: kwargs.get(col) for col in cols}

        for col, strategy in strategies.items():
            if strategy == 'human':
                player = SantoriniPlayerHuman(col)
            elif strategy == 'random':
                player = SantoriniPlayerRandom(col)
            elif strategy == 'heuristic':
                player = SantoriniPlayerHeuristic(col)
            else:
                player = None
            players.append(player)

        return players

    def run(self) -> None:
        print(self._players)
        print(self._board)
