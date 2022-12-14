"""Santorini board module"""

from .tile import SantoriniTile
from .worker import SantoriniWorker
from .player import SantoriniPlayerBase
from .constants import DIRECTIONS

class SantoriniBoard:

    def __init__(self, dim=(5, 5), workers=None) -> None:
        self._dim = dim
        self._tiles: list[list[SantoriniTile]] = self._create_tiles()
        self._workers: list[SantoriniWorker] = workers
        if workers:
            self._init_workers()
    
    def _create_tiles(self) -> list[list[SantoriniTile]]:
        tiles = []
        for _ in range(self._dim[0]):
            row = []
            for _ in range(self._dim[1]):
                row.append(SantoriniTile())
            tiles.append(row)
        return tiles

    def _get_tile(self, location: tuple) -> SantoriniTile:
        return self._tiles[location[0]][location[1]]
    
    def _init_workers(self) -> None:
        for worker in self._workers:
            self._worker_move(worker, (0, 0))

    def get_worker_names(self, player: SantoriniPlayerBase) -> list[str]:

        workers = [worker for worker in self._workers if worker.col == player.col]
        names = [worker.name for worker in workers]
        return names

    def implement_move(self, chosen: tuple[str, str, str]):

        name, move, build = chosen

        worker = [worker for worker in self._workers if worker.name == name][0]

        move_direction = DIRECTIONS.get(move)
        build_direction = DIRECTIONS.get(build)

        self._worker_move(worker, move_direction)
        self._worker_build(worker, build_direction)

    def get_valid_moves(self, player: SantoriniPlayerBase) -> list[tuple[str, str, str]]:

        workers = [worker for worker in self._workers if worker.col == player.col]

        valid_moves = []
        for worker in workers:
            worker_moves = self._get_worker_moves(worker)
            if worker_moves:
                valid_moves += worker_moves
        return valid_moves

    def _get_worker_moves(self, work: SantoriniWorker) -> list[tuple[str, str, str]]:

        worker_moves = []

        name = work.name
        src = work.location

        # unoccupy the original space to allow building after moving
        src_tile = self._get_tile(src)
        src_tile.worker = None

        # all possible moves
        for dir1, tup1 in DIRECTIONS.items():
            dst1 = tuple(i + j for i,j in zip(src, tup1))

            # valid moves (early termination condition)
            if self._validate_move(src, dst1):

                # possible builds
                for dir2, tup2 in DIRECTIONS.items():
                    dst2 = tuple(i + j for i,j in zip(dst1, tup2))

                    # valid builds (early termination condition)
                    if self._validate_build(dst2):

                        # valid move + valid build discovered
                        worker_moves.append((name, dir1, dir2))

        # re-occupy the original space
        src_tile.worker = work
        
        return worker_moves

    def _validate_move(self, src: tuple, dst: tuple) -> bool:

        src_tile = self._get_tile(src)

        if (dst[0] < 0 or dst[0] >= self._dim[0]): return False
        if (dst[1] < 0 or dst[1] >= self._dim[1]): return False

        dst_tile = self._get_tile(dst)

        if not src_tile.reaches(dst_tile): return False
        if dst_tile.occupied(): return False

        return True

    def _validate_build(self, dst: tuple) -> bool:

        if (dst[0] < 0 or dst[0] >= self._dim[0]): return False
        if (dst[1] < 0 or dst[1] >= self._dim[1]): return False

        dst_tile = self._get_tile(dst)

        if dst_tile.occupied(): return False

        return True

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
