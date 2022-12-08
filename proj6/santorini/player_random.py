from .player import SantoriniPlayer

class SantoriniPlayerRandom(SantoriniPlayer):

    def __init__(self) -> None:
        pass

    def take_turn(self):
        print('Random takes turn')
