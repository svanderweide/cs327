from abc import ABC, abstractmethod
from .worker import SantoriniWorker

class SantoriniPlayer(ABC):

    def __init__(self, col) -> None:
        super().__init__()
        self._col = col
        self._workers = self._create_workers()

    def _create_workers(self) -> list[SantoriniWorker]:
        return None

    @abstractmethod
    def take_turn(self):
        pass
