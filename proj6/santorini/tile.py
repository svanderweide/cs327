"""Santorini board tile module"""

from .worker import SantoriniWorker
from .structure import SantoriniStructure
from .exceptions import InvalidBuildException, InvalidMoveException

class SantoriniTile():

    def __init__(self) -> None:
        self._worker = None
        self._structure = SantoriniStructure()

    def _get_worker(self) -> SantoriniWorker | None:
        return self._worker

    def _set_worker(self, worker: SantoriniWorker) -> None:
        if worker is not None:
            if self._worker or self._structure.domed():
                raise InvalidMoveException()
        self._worker = worker
    
    worker = property(_get_worker, _set_worker)
    
    def build(self) -> None:
        if self.worker or self._structure.domed():
            raise InvalidBuildException()
        self._structure.build()
    
    def reaches(self, other) -> bool:
        return self._structure.reaches(other._structure)

    def __str__(self) -> str:
        tile = ''
        tile += str(self._structure) if self._structure else ' '
        tile += str(self._worker) if self._worker else ' '
        return tile
