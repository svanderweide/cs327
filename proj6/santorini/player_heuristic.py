from .player import SantoriniPlayer

class SantoriniPlayerHeuristic(SantoriniPlayer):

    def take_turn(self):
        print('Heuristic takes turn')
