"""
SantoriniPlayer module
----------------------
Implements the various types of players (human, random, heuristic) allowed in the
basic Santorini game required by hw6 with easy extension if additional are desired
"""

from abc import ABC, abstractmethod
from random import choice

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
        """
        Template method for a player's turn that requires the player subclasses
        to implement the '_make_choice' method to fill in the template
        """

        # select worker, move, and build (subclass-defined)
        chosen: tuple[str, str, str] = self._make_choice(board)

        # implement the move on the board
        board.implement_move(chosen)

    def base_get_description(self, board) -> str:
        """Returns a description of the player for the given board"""
        worker_names = board.get_worker_names(self)
        workers = ''.join(sorted(worker_names))
        return f'{self} ({workers})'

    def get_description(self, board) -> str:
        """Used to allow the heuristic score decorator without multiple decorators"""
        return self.base_get_description(board)

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
            return chosen_worker == move['name']

        all_workers = board.get_worker_names()

        while True:
            print('Select a worker to move')
            chosen_worker = input()
            if chosen_worker not in all_workers:
                print('Not a valid worker')
                continue
            if chosen_worker not in self._names:
                print('That is not your worker')
                continue
            filtered_moves = [move for move in valid_moves if filter_move(move)]
            if filtered_moves:
                break

        return chosen_worker, filtered_moves

    def _select_move(self, valid_moves) -> tuple[str, list[tuple[str, str, str]]]:

        def filter_move(move: tuple[str, str, str]):
            return chosen_move == move['move']

        while True:
            print('Select a direction to move (n, ne, e, se, s, sw, w, nw)')
            chosen_move = input()
            if chosen_move not in DIRECTIONS:
                print('Not a valid direction')
                continue
            filtered_moves = [move for move in valid_moves if filter_move(move)]
            if filtered_moves:
                break
            print(f'Cannot move {chosen_move}')

        return chosen_move, filtered_moves

    def _select_build(self, valid_moves) -> tuple[str, list[tuple[str, str, str]]]:

        def filter_move(move: tuple[str, str, str]):
            return chosen_build == move['build']

        while True:
            print('Select a direction to build (n, ne, e, se, s, sw, w, nw)')
            chosen_build = input()
            if chosen_build not in DIRECTIONS:
                print('Not a valid direction')
                continue
            filtered_moves = [move for move in valid_moves if filter_move(move)]
            if filtered_moves:
                break
            print(f'Cannot build {chosen_build}')

        return chosen_build, filtered_moves

    def _make_choice(self, board) -> tuple[str, str, str]:

        # get all valid moves
        valid_moves = board.get_valid_moves(self)

        # independently select worker, move, and build
        chosen_name, valid_moves = self._select_worker(valid_moves, board)
        chosen_move, valid_moves = self._select_move(valid_moves)
        chosen_build, valid_moves = self._select_build(valid_moves)

        return chosen_name, chosen_move, chosen_build


class SantoriniPlayerRandom(SantoriniPlayerBase):
    """
    SantoriniPlayerRandom
    ---------------------
    Concrete player class that selects a move at random
    """

    def _make_choice(self, board) -> tuple[str, str, str]:

        # get all the valid moves
        valid_moves = board.get_valid_moves(self)

        # randomly select move
        chosen = choice(valid_moves)

        # extract components of the chosen move
        chosen_name = chosen['name']
        chosen_move = chosen['move']
        chosen_build = chosen['build']

        # print the move (only required for AI players)
        print(f'{chosen_name},{chosen_move},{chosen_build}')

        return chosen_name, chosen_move, chosen_build


class SantoriniPlayerHeuristic(SantoriniPlayerBase):
    """
    SantoriniPlayerHeuristic
    ------------------------
    Concrete player class that selects a move according to the move's heuristic score,
    breaking ties between moves with the maximum score at random
    """

    _multipliers = {
        'height': 3,
        'center': 2,
        'distance': 1,
    }

    def _calculate_score(self, scores: tuple):

        # compute the weighted heuristic scores
        heuristic_score = 0
        heuristic_score += scores[0] * self._multipliers['height']
        heuristic_score += scores[1] * self._multipliers['center']
        heuristic_score += scores[2] * self._multipliers['distance']

        return heuristic_score

    def _make_choice(self, board) -> tuple[str, str, str]:

        # get all the valid moves (and their heuristic scores)
        valid_moves = board.get_valid_moves(self, heuristic=True)

        # compute the weighted scores
        for move in valid_moves:
            move['score'] = self._calculate_score(move['score'])

        # calculate highest heuristic score
        highest_heuristic_score = max(move['score'] for move in valid_moves)

        # get the moves with the highest heuristic score
        valid_moves = [move for move in valid_moves if move['score'] == highest_heuristic_score]

        # randomly select remove from the remaining
        chosen = choice(valid_moves)

        # extract components of the chosen move
        chosen_name = chosen['name']
        chosen_move = chosen['move']
        chosen_build = chosen['build']

        # print the move (only required for AI players)
        print(f'{chosen_name},{chosen_move},{chosen_build}')

        return chosen_name, chosen_move, chosen_build
