from .board import SantoriniBoard
from .player import SantoriniPlayer
from .architect import SantoriniArchitect
from .constants import DIRECTIONS, DIRECTION_NAMES
from .exceptions import InvalidBuildException, InvalidMoveException

class SantoriniPlayerHuman(SantoriniPlayer):

    def _select_architect(self, board: SantoriniBoard):

        architects = board.get_architects(self._col)

        while True:
            print('Select a architect to move')
            architect_name = input()
            filtered = [arch for arch in architects if arch.has_name(architect_name)]
            try:
                selected = filtered[0]
            except IndexError:
                print('Not a valid architect')
            else:
                break
        return selected

    def _select_move(self, architect: SantoriniArchitect, board: SantoriniBoard):

        while True:
            print(f'Select a direction to move ({DIRECTION_NAMES})')
            move_direction = input()
            try:
                board.architect_move(architect, move_direction)
            except KeyError:
                print('Not a valid direction')
            except InvalidMoveException:
                print(f'Cannot move {move_direction}')
            else:
                break

    def _select_build(self, architect: SantoriniArchitect, board: SantoriniBoard):

        while True:
            print(f'Select a direction to build ({DIRECTION_NAMES})')
            build_direction = input()
            try:
                board.architect_build(architect, build_direction)
            except KeyError:
                print('Not a valid direction')
            except InvalidBuildException:
                print(f'Cannot move {build_direction}')
            else:
                break

    def take_turn(self, board: SantoriniBoard):

        architect = self._select_architect(board)
        self._select_move(architect)
        self._select_build(architect)
