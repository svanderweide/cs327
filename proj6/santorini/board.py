"""Santorini board module"""

from .tile import SantoriniTile
from .worker import SantoriniWorker
from .constants import WORKERS, DIRECTIONS
from .exceptions import InvalidBuildException, InvalidMoveException

class FixedWidthList(list):

    def __getitem__(self, idx):
        if idx < 0:
            raise IndexError(f'Expected positive index: got {idx}')
        return super().__getitem__(idx)

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

    # loads from constants file for 2-player CLI version
    def _create_workers(self) -> list[SantoriniWorker]:

        workers = []
        for template in WORKERS:
            col  = template['col']
            name = template['name']
            pos  = template['pos']
            worker = SantoriniWorker(col, name)
            self.worker_move(worker, pos)
            workers.append(worker)
        return workers

    def get_valid_moves(self, name: str) -> list[(str, tuple)]:

        worker = [worker for worker in self._workers if worker._name == name][0]

        valid_moves = []
        for direction in DIRECTIONS.values():
            try:
                self.worker_move(worker, direction)
            except InvalidMoveException:
                continue
            else:
                self.worker_move(worker, tuple(-val for val in direction))
                valid_moves.append((worker._name, direction))
        return valid_moves


        worker4 = SantoriniWorker('blue', 'Z')
        self.worker_move(worker4, (3, 3))

        return [worker1, worker2, worker3, worker4]

    def worker_move(self, worker: SantoriniWorker, direction: tuple) -> None:

        src_location = worker.location
        dst_location = tuple(i + j for i,j in zip(src_location, direction))

        src_tile = self._get_tile(src_location)
        try:
            dst_tile = self._get_tile(dst_location)
        except IndexError:
            raise InvalidMoveException()
        else:
            if not src_tile.reaches(dst_tile):
                raise InvalidMoveException()
            dst_tile.worker = worker
            src_tile.worker = None
            worker.location = dst_location

    def worker_build(self, worker: SantoriniWorker, direction: tuple) -> None:

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
