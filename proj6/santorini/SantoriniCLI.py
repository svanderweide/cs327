"""
Santorini game driver module

Responsible for setting up, launching, and monitoring
the state of the game for termination conditions
"""

from santorini.board import SantoriniBoard
from santorini.worker import SantoriniWorker
from santorini.player import (SantoriniPlayerHuman, SantoriniPlayerRandom, SantoriniPlayerHeuristic)

class SantoriniCLI():

    def __init__(self, **kwargs) -> None:
        self._players = self._create_players(**kwargs)
        self._board = SantoriniBoard(workers=self._create_workers())

    def _create_players(self, **kwargs) -> list:

        players = []

        # hard-coded for 2-player CLI version
        cols = ['white', 'blue']

        # not hard-coded for 2-player CLI version
        # but depends on hard-coded values above
        strategies = {col: kwargs.get(col) for col in cols}

        for col, strategy in strategies.items():
            if strategy == 'human':
                player = SantoriniPlayerHuman(col)
            elif strategy == 'random':
                player = SantoriniPlayerRandom(col)
            elif strategy == 'heuristic':
                player = SantoriniPlayerHeuristic(col)
            players.append(player)

        return players

    def _create_workers(self) -> list[SantoriniWorker]:

        # hard-coded for 2-player CLI version
        workers = [
            SantoriniWorker('white', 'A', (3, 1)),
            SantoriniWorker('white', 'B', (1, 3)),
            SantoriniWorker('blue', 'Y', (1, 1)),
            SantoriniWorker('blue', 'Z', (3, 3)),
        ]
        
        return workers

    def run(self) -> None:

        idx = 0
        player_len = len(self._players)
        turn = 1

        while True:
            player = self._players[idx]
            print(self._board)
            print(f'Turn: {turn}, ', end='')
            player.print_description(self._board)
            player.take_turn(self._board)
            idx = (idx + 1) % player_len
            turn += 1
