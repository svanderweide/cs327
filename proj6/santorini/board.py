"""
Board module
------------
Implements the Santorini game board itself, which maintains most of the game's
validation, logical state, and functions as an interface for the players
"""

from math import inf
from re import match

from .tile import SantoriniTile
from .worker import SantoriniWorker
from .player import SantoriniPlayerBase
from .constants import DIRECTIONS

class SantoriniBoard:
    """
    SantoriniBoard
    --------------
    Responsible for generating and validating possible moves,
    maintaining the displayed interface, calculating heuristic scores
    for players and moves, and checking for termination conditions
    """

    def __init__(self, dim=(5, 5), workers=None) -> None:
        self._dim = dim
        self._tiles: list[list[SantoriniTile]] = self._create_tiles()
        self._workers: list[SantoriniWorker] = workers
        if workers:
            self._init_workers()

    # SET-UP METHODS

    def _create_tiles(self) -> list[list[SantoriniTile]]:
        tiles = []
        for _ in range(self._dim[0]):
            row = []
            for _ in range(self._dim[1]):
                row.append(SantoriniTile())
            tiles.append(row)
        return tiles

    def _init_workers(self) -> None:
        for worker in self._workers:
            self._worker_move(worker, (0, 0))

    # AUXILIARY METHODS

    def _get_tile(self, location: tuple) -> SantoriniTile:
        return self._tiles[location[0]][location[1]]

    def get_worker_names(self, player: SantoriniPlayerBase=None) -> list[str]:
        """Generate a list of workers on the board where the colors are the same"""

        col = player.col if player else ''
        names = [worker.name for worker in self._workers if match(col, worker.col)]
        return names

    def __str__(self) -> str:

        board = ''
        row_division = '+--' * self._dim[1] + '+'

        board += row_division
        for row in range(self._dim[0]):
            board += '\n'
            board += '|'
            for col in range(self._dim[1]):
                board += str(self._tiles[row][col])
                board += '|'
            board += '\n'
            board += row_division

        return board

    # CALCULATION METHODS

    def get_heuristic_score(self, player: SantoriniPlayerBase, infinite=False) -> tuple:
        """Return the player's current heuristic score"""

        # get current location of player's workers
        player_locations = [worker.location for worker in self._workers if worker.col == player.col]

        # get current location of opponent's workers
        opp_locations = [worker.location for worker in self._workers if worker.col != player.col]

        return self._calculate_heuristic_score(player_locations, opp_locations, infinite)

    def _calculate_heuristic_score(self, player_locations, opponent_locations, infinite):

        heights = [self._get_tile(location).height_score for location in player_locations]
        if infinite:
            heights = [height if height != 3 else inf for height in heights]
        height_score = sum(heights)

        centers = [self._get_distance(location, (2, 2)) for location in player_locations]
        center_score = 4 - sum(centers)

        distances = []
        for loc2 in opponent_locations:
            distances.append(min(self._get_distance(loc1, loc2) for loc1 in player_locations))
        distance_score = 8 - sum(distances)

        return (height_score, center_score, distance_score)

    def _get_distance(self, location1: tuple, location2: tuple) -> int:
        diffs = [abs(loc1 - loc2) for loc1, loc2 in zip(location1, location2)]
        return max(diffs)

    # TERMINATION METHODS

    def check_termination(self, player: SantoriniPlayerBase) -> bool:
        """Check whether the game's termination conditions are active"""

        for worker in self._workers:
            tile = self._get_tile(worker.location)
            if tile.is_victory_level():
                return True

        return not bool(self.get_valid_moves(player))

    # MOVE GENERATION METHODS

    def get_valid_moves(self, player: SantoriniPlayerBase,
                              heuristic=False) -> list[dict]:
        """Generate a list of the player's valid moves (and heuristic scores)"""

        workers = [worker for worker in self._workers if worker.col == player.col]

        valid_moves = []
        for worker in workers:
            worker_moves = self._get_worker_moves(player, worker, heuristic)
            if worker_moves:
                valid_moves += worker_moves
        return valid_moves

    def _get_worker_moves(self, player: SantoriniPlayerBase,
                                work: SantoriniWorker,
                                heuristic: bool) -> list[dict]:

        worker_moves = []

        src = work.location

        # unoccupy the original space to allow building after moving
        src_tile = self._get_tile(src)
        src_tile.worker = None

        # all possible moves
        for dir1, tup1 in DIRECTIONS.items():
            dst1 = tuple(i + j for i,j in zip(src, tup1))

            # valid moves (early termination condition)
            if self._validate_move(src, dst1):

                work.location = dst1
                heuristic_score = self.get_heuristic_score(player, True) if heuristic else None
                work.location = src

                # possible builds
                for dir2, tup2 in DIRECTIONS.items():
                    dst2 = tuple(i + j for i,j in zip(dst1, tup2))

                    # valid builds (early termination condition)
                    if self._validate_build(dst2):

                        valid_move = {
                            'name': work.name,
                            'move': dir1,
                            'build': dir2,
                            'score': heuristic_score
                        }

                        # valid move + valid build discovered
                        worker_moves.append(valid_move)

        # re-occupy the original space
        src_tile.worker = work

        return worker_moves

    # MOVE METHODS

    def implement_move(self, chosen: tuple[str, str, str]):
        """Implement the chosen move on the board

        Args:
            tuple[str, str, str]:   a tuple of worker name, move direction,
                                    and build direction to be implemented
        """

        name, move, build = chosen

        worker = [worker for worker in self._workers if worker.name == name][0]

        move_direction = DIRECTIONS.get(move)
        build_direction = DIRECTIONS.get(build)

        self._worker_move(worker, move_direction)
        self._worker_build(worker, build_direction)

    def _worker_move(self, worker: SantoriniWorker, direction: tuple) -> None:

        src_location = worker.location
        dst_location = tuple(i + j for i,j in zip(src_location, direction))

        # assumes error checking has already occurred
        src_tile = self._get_tile(src_location)
        dst_tile = self._get_tile(dst_location)

        # update relevant worker and tiles
        src_tile.worker = None
        dst_tile.worker = worker
        worker.location = dst_location

    def _worker_build(self, worker: SantoriniWorker, direction: tuple) -> None:

        src_location = worker.location
        dst_location = tuple(i + j for i,j in zip(src_location, direction))

        # assumes error checking has already occurred
        dst_tile = self._get_tile(dst_location)
        dst_tile.build()

    # VALIDATION METHODS

    def _validate_move(self, src: tuple, dst: tuple) -> bool:

        src_tile = self._get_tile(src)

        if (dst[0] < 0 or dst[0] >= self._dim[0]):
            return False
        if (dst[1] < 0 or dst[1] >= self._dim[1]):
            return False

        dst_tile = self._get_tile(dst)

        if not src_tile.reaches(dst_tile):
            return False
        if dst_tile.is_occupied():
            return False

        return True

    def _validate_build(self, dst: tuple) -> bool:

        if (dst[0] < 0 or dst[0] >= self._dim[0]):
            return False
        if (dst[1] < 0 or dst[1] >= self._dim[1]):
            return False

        dst_tile = self._get_tile(dst)

        if dst_tile.is_occupied():
            return False

        return True
