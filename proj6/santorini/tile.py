"""Santorini board tile module"""

from .worker import SantoriniWorker

class SantoriniTile():

    _limit_level = 4

    def __init__(self) -> None:
        self._worker = None
        self._level = 0

    def _get_worker(self) -> SantoriniWorker | None:
        return self._worker

    def _set_worker(self, worker: SantoriniWorker) -> None:
        self._worker = worker
    
    worker = property(_get_worker, _set_worker)
    
    def build(self) -> None:
        self._level += 1
        
    def undo_build(self) -> None:
        self._level -= 1

    def is_occupied(self) -> bool:
        return self.worker or self._level == SantoriniTile._limit_level

    def is_victory_level(self) -> bool:
        return self._level + 1 == SantoriniTile._limit_level

    def reaches(self, other) -> bool:
        return other._level - self._level <= 1

    def __str__(self) -> str:
        return f'{self._level}{self._worker or " "}'
