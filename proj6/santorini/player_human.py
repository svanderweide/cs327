from .player import SantoriniPlayer

class SantoriniPlayerHuman(SantoriniPlayer):

    def take_turn(self):
        print('Human takes turn')
