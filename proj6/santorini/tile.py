"""
Tile module
-----------
Implements the tile class responsible for maintaining a single tile
on the Santorini game board with same validation logic embedded
"""

from .worker import SantoriniWorker

class SantoriniTile():
    """
    SantoriniTile
    -------------
    Maintains and allows access (through certain methods) to its
    current height, state of occupancy, and occupant (i.e., worker)
    for the game board to print itself and to perform move validation
    """

    _limit_level = 4

    def __init__(self) -> None:
        self._worker = None
        self._level = 0

    def _get_worker(self) -> SantoriniWorker | None:
        return self._worker

    def _set_worker(self, worker: SantoriniWorker) -> None:
        self._worker = worker

    worker = property(_get_worker, _set_worker)

    def _get_level(self) -> int:
        return self._level

    height_score = property(_get_level)

    def build(self) -> None:
        """Build on the tile"""
        self._level += 1

    def is_occupied(self) -> bool:
        """Returns whether the tile has a worker or is domed"""
        return self.worker or self._level == SantoriniTile._limit_level

    def is_victory_level(self) -> bool:
        """Returns whether a worker on the tile ends the game"""
        return self._level + 1 == SantoriniTile._limit_level

    def reaches(self, other) -> bool:
        """Returns wheter the tile [other] is reachable from this tile"""
        return other._level - self._level <= 1

    def __str__(self) -> str:
        return f'{self._level}{self._worker or " "}'
