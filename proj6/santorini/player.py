"""
SantoriniPlayer module
----------------------
Implements the various types of players (human, random, heuristic) allowed in the
basic Santorini game required by hw6 with easy extension if additional are desired
"""

from abc import ABC, abstractmethod
from random import choice

from .worker import SantoriniWorker
from .constants import DIRECTIONS


class SantoriniPlayerBase(ABC):
    """
    SantoriniPlayerBase
    -------------------
    Abstract player class with abstract method for taking a turn
    """

    def __init__(self, col: str, names: list[str]) -> None:
        super().__init__()
        self._col = col
        self._names = names

    def _get_col(self) -> str:
        return self._col

    col = property(_get_col)

    @abstractmethod
    def _make_choice(self, board) -> None:
        pass

    def take_turn(self, board) -> None:

        # select worker, move, and build (subclass-defined)
        choice: tuple[str, str, str] = self._make_choice(board)

        # implement the move on the board
        board.implement_move(choice)

    def print_description(self, board) -> None:
        valid_moves = board.get_worker_names(self)
        workers = set(move[0] for move in valid_moves)
        workers = ''.join(sorted(workers))
        print(f'{self} ({workers})')

    def __str__(self) -> str:
        return f'{self._col}'


class SantoriniPlayerHuman(SantoriniPlayerBase):
    """
    SantoriniPlayerHuman
    --------------------
    Concrete player class that prompts the user to choose a move
    """

    def _select_worker(self, valid_moves, board) -> tuple[str, list[tuple[str, str, str]]]:

        def filter_move(move: tuple[str, str, str]):
            return chosen_worker == move[0]

        all_workers = board.get_worker_names()

        while True:
            print('Select a worker to move')
            chosen_worker = input()
            if chosen_worker not in all_workers:
                print('Not a valid worker')
                continue
            elif chosen_worker not in self._names:
                print('That is not your worker')
                continue
            filtered_moves = [move for move in valid_moves if filter_move(move)]
            if filtered_moves:
                break

        return chosen_worker, filtered_moves

    def _select_move(self, valid_moves) -> tuple[str, list[tuple[str, str, str]]]:

        def filter_move(move: tuple[str, str, str]):
            return chosen_move == move[1]

        while True:
            print('Select a direction to move (n, ne, e, se, s, sw, w, nw)')
            chosen_move = input()
            if chosen_move not in DIRECTIONS.keys():
                print('Not a valid direction')
                continue
            filtered_moves = [move for move in valid_moves if filter_move(move)]
            if filtered_moves:
                break
            else:
                print(f'Cannot move {chosen_move}')
        
        return chosen_move, filtered_moves

    def _select_build(self, valid_moves) -> tuple[str, list[tuple[str, str, str]]]:

        def filter_move(move: tuple[str, str, str]):
            return chosen_build == move[2]

        while True:
            print('Select a direction to build (n, ne, e, se, s, sw, w, nw)')
            chosen_build = input()
            if chosen_build not in DIRECTIONS.keys():
                print('Not a valid direction')
                continue
            filtered_moves = [move for move in valid_moves if filter_move(move)]
            if filtered_moves:
                break
            else:
                print(f'Cannot build {chosen_build}')

        return chosen_build, filtered_moves

    def _make_choice(self, board) -> tuple[str, str, str]:
        valid_moves = board.get_valid_moves(self)
        chosen_worker, valid_moves = self._select_worker(valid_moves, board)
        chosen_move,   valid_moves = self._select_move(valid_moves)
        chosen_build,  valid_moves = self._select_build(valid_moves)
        return chosen_worker, chosen_move, chosen_build


class SantoriniPlayerRandom(SantoriniPlayerBase):
    """
    SantoriniPlayerRandom
    ---------------------
    Concrete player class that selects a move at random
    """

    def _make_choice(self, board) -> tuple[str, str, str]:
        valid_moves = board.get_valid_moves(self)
        chosen = choice(valid_moves)
        print(','.join(chosen))
        return chosen


class SantoriniPlayerHeuristic(SantoriniPlayerBase):
    """
    SantoriniPlayerHeuristic
    ------------------------
    Concrete player class that selects a move according to the move's heuristic score
    """

    def _make_choice(self, valid_moves: dict[SantoriniWorker, dict[str, list[str]]]) -> None:
        return super()._make_choice(valid_moves)
