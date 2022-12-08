from .player import SantoriniPlayer

class SantoriniPlayerHuman(SantoriniPlayer):

    def __init__(self) -> None:
        pass

    def take_turn(self):
        print('Human takes turn')
