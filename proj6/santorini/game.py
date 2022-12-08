from .board import SantoriniBoard
from .player import SantoriniPlayer
from .player_human import SantoriniPlayerHuman
from .player_random import SantoriniPlayerRandom
from .player_heuristic import SantoriniPlayerHeuristic

class SantoriniGame:

    def __init__(self, **kwargs) -> None:
        self._players = self._create_players(**kwargs)
        self._board = SantoriniBoard((5,5), self._players)
        self._turn_num = 1
    
    # only works for 2-player CLI version
    def _create_players(self, **kwargs) -> list[SantoriniPlayer]:

        players: list[SantoriniPlayer] = []

        # only works for 2-player CLI version
        player_cols = ['white', 'blue']
        
        player_types = {col: kwargs.get(col) for col in player_cols}

        for col, type in player_types.items():
            if type == 'human':
                player = SantoriniPlayerHuman(col)
            elif type == 'random':
                player = SantoriniPlayerRandom(col)
            elif type == 'heuristic':
                player = SantoriniPlayerHeuristic(col)
            players.append(player)

        return players

    def run(self) -> None:
        done: bool = False
        while not done:
            done = self._turn()

    def _turn(self) -> bool:
        for player in self._players:
            print(self._board)

            # TODO: Fix this ugly print statement (class?)
            print(f'Turn: {self._turn_num}, {player} ({"".join([str(arch) for arch in player.get_architects(self._board)])})')

            player.take_turn(self._board)
            self._turn_num += 1
        return True
