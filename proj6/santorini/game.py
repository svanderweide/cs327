from .board import SantoriniBoard
from .player import SantoriniPlayer
from .player_human import SantoriniPlayerHuman
from .player_random import SantoriniPlayerRandom
from .player_heuristic import SantoriniPlayerHeuristic

class SantoriniGame:

    def __init__(self, *args, **kwargs):
        self._board = SantoriniBoard()
    
    def run(self):
        print(self._board)
