from .architect import SantoriniArchitect
from .structure import SantoriniStructure

class SantoriniBoardTile:

    def __init__(self) -> None:
        self._architect: SantoriniArchitect = None
        self._structure = SantoriniStructure()
    
    def _set_architect(self, architect: SantoriniArchitect) -> None:
        self._architect = architect
    
    architect = property(None, _set_architect)
    
    def build(self) -> None:
        self._structure.build()

    def reaches(self, other) -> None:
        return self._structure.reaches(other._structure)

    def __str__(self) -> str:
        tile = ''
        tile += str(self._structure) if self._structure else ' '
        tile += str(self._architect) if self._architect else ' '
        return tile
