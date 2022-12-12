"""Santorini board module"""

from .tile import SantoriniTile
from .worker import SantoriniWorker
from .exceptions import InvalidBuildException, InvalidMoveException

class SantoriniBoard:

    def __init__(self, dim: tuple) -> None:
        self._dim = dim
        self._tiles = self._create_tiles()
        self._workers = self._create_workers()

    def _get_tile(self, location: tuple) -> SantoriniTile:
        return self._tiles[location[0]][location[1]]
    
    def _create_tiles(self) -> list[list[SantoriniTile]]:
        
        tiles = FixedWidthList()
        for _ in range(self._dim[0]):
            row = FixedWidthList()
            for _ in range(self._dim[1]):
                row.append(SantoriniTile())
            tiles.append(row)
        return tiles

    # only works for 2-player CLI version
    def _create_workers(self) -> list[SantoriniWorker]:

        worker1 = SantoriniWorker('white', 'A')
        self.worker_move(worker1, (3, 1))

        worker2 = SantoriniWorker('white', 'B')
        self.worker_move(worker2, (1, 3))

        worker3 = SantoriniWorker('blue', 'Y')
        self.worker_move(worker3, (1, 1))

        worker4 = SantoriniWorker('blue', 'Z')
        self.worker_move(worker4, (3, 3))

        return [worker1, worker2, worker3, worker4]

    
    def worker_move(self, worker: SantoriniWorker, direction: tuple):

        src_location = worker.location
        dst_location = tuple(i + j for i,j in zip(src_location, direction))

        try:
            dst_tile = self._get_tile(dst_location)
        except IndexError:
            raise InvalidMoveException()
        else:
            dst_tile.worker = worker
            worker.location = dst_location

    def worker_build(self, worker: SantoriniWorker, direction: tuple):

        src_location = worker.location
        dst_location = tuple(i + j for i,j in zip(src_location, direction))

        try:
            dst_tile = self._get_tile(dst_location)
        except IndexError:
            raise InvalidBuildException()
        else:
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

class FixedWidthList(list):

    def __getitem__(self, idx):
        if idx < 0:
            raise IndexError(f'Expected positive index: got {idx}')
        return super().__getitem__(idx)
