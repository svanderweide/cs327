from abc import ABC, abstractmethod
from .worker import SantoriniWorker

class SantoriniPlayer(ABC):

    def __init__(self, col: str, workers: list[SantoriniWorker]) -> None:
        super().__init__()
        self._col = col
        self._workers = workers

    def __str__(self) -> str:
        workers = ''.join([str(worker) for worker in self._workers])
        return f'{self._col} ({workers})'

    @abstractmethod
    def take_turn(self):
        pass
