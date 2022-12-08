from .player import SantoriniPlayer

class SantoriniPlayerHeuristic(SantoriniPlayer):

    def __init__(self) -> None:
        pass

    def take_turn(self):
        print('Heuristic takes turn')
