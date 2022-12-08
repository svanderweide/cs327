from .worker import SantoriniWorker
from .structure import SantoriniStructure

class SantoriniBoardTile:

    def __init__(self) -> None:
        self._worker: SantoriniWorker = None
        self._structure = SantoriniStructure()
    
    def occupy(self, worker: SantoriniWorker) -> None:
        self._worker = worker
    
    def build(self) -> None:
        self._structure.build()

    def __str__(self) -> str:
        tile = ''
        tile += str(self._structure) if self._structure else ' '
        tile += str(self._worker) if self._worker else ' '
        return tile
