from abc import ABC, abstractmethod
from .architect import SantoriniArchitect

class SantoriniPlayer(ABC):

    def __init__(self, col: str) -> None:
        super().__init__()
        self._col = col

    def _get_color(self) -> str:
        return self._col
    
    col = property(_get_color)

    def get_architects(self, board) -> list[SantoriniArchitect]:
        return board.get_architects(self._col)

    def __str__(self) -> str:
        return f'{self._col}'

    @abstractmethod
    def take_turn(self, board):
        pass
